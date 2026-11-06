#!/usr/bin/env python3
"""Fetch or verify pinned guidance sources. Does not execute installers or register skills."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

BASE = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', *args],
                          check=True, capture_output=True, text=True).stdout.strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch', action='store_true', help='Fetch absent pinned checkouts into ignored vendor/')
    args = parser.parse_args()
    manifest = json.loads((BASE / 'research/skill-lock.json').read_text())
    results = []
    for source in manifest['sources']:
        repository = source['repository']
        commit = source['commit']
        destination = (BASE / source['checkout_path']).resolve()
        vendor = (BASE / 'vendor/agent-skills').resolve()
        if not destination.is_relative_to(vendor) or destination == vendor:
            raise ValueError('Skill checkout must be inside vendor/agent-skills')
        if not re.fullmatch(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?', repository):
            raise ValueError('Only explicit HTTPS GitHub repository sources are supported')
        if not re.fullmatch(r'[0-9a-f]{40}', commit):
            raise ValueError('An exact 40-character commit SHA is required')
        if not destination.exists():
            if not args.fetch:
                results.append({'repository': repository, 'state': 'not_fetched', 'next': 'Run with --fetch'})
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            git('clone', '--no-checkout', repository, str(destination))
            git('-C', str(destination), 'checkout', '--detach', commit)
        if git('-C', str(destination), 'rev-parse', 'HEAD') != commit:
            raise ValueError(f'Checkout revision differs from lock: {repository}; existing work was left unchanged')
        if git('-C', str(destination), 'status', '--porcelain'):
            raise ValueError(f'Checkout has local changes: {repository}; existing work was left unchanged')
        checked = 0
        for record in source.get('reviewed_files', []):
            path = (destination / record['path']).resolve()
            if not path.is_relative_to(destination):
                raise ValueError('Reviewed file resolves outside its repository')
            if hashlib.sha256(path.read_bytes()).hexdigest() != record['sha256']:
                raise ValueError(f'Reviewed file hash differs: {repository}/{record["path"]}')
            checked += 1
        results.append({'repository': repository, 'state': 'pinned_checkout_verified',
                        'commit': commit, 'reviewed_files_verified': checked,
                        'global_registration': False})
    print(json.dumps(results, indent=2))
    return 0 if all(r['state'] == 'pinned_checkout_verified' for r in results) else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print(f'Skill source check failed: {error}', file=sys.stderr)
        sys.exit(1)
