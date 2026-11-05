#!/usr/bin/env python3
"""Prepare local video projects and provider prompts. Makes no network calls."""
import argparse
import csv
import json
import math
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[1]
TRACKS = ('heuro', 'personal')
PROVIDERS = ('synthesia', 'google', 'descript', 'remotion', 'comfyui')
STATES = ('queued', 'running', 'needs_answer', 'done', 'failed', 'cancelled')
ACTIVE = ('queued', 'running', 'needs_answer')
SHOT_FIELDS = ('shot_id', 'start_seconds', 'duration_seconds', 'kind', 'narration', 'visual', 'on_screen_text')
ASSET_FIELDS = ('asset_id', 'kind', 'stable_storage_id', 'sha256', 'rights', 'status')
JOB_FIELDS = ('provider', 'job_id', 'state', 'conversation_id', 'url')
ROUTES = {'speaking': 'synthesia', 'generated_scene': 'google', 'product_capture': 'supplied_footage',
          'motion_graphic': 'remotion', 'supplied_footage': 'supplied_footage'}


def read_json(path, fallback=None):
    if not path.exists() and fallback is not None:
        return fallback
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f'Cannot read JSON from {path}: {error}') from error


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def csv_rows(path, fields):
    try:
        with path.open(encoding='utf-8', newline='') as handle:
            reader = csv.DictReader(handle)
            if tuple(reader.fieldnames or ()) != fields:
                raise ValueError(f'{path.name} must use columns: {", ".join(fields)}')
            rows = list(reader)
    except OSError as error:
        raise ValueError(f'Cannot read {path}: {error}') from error
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise ValueError(f'{path.name} contains a row with the wrong number of columns')
    return rows


def write_csv(path, fields, rows):
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def identifier(value, label):
    allowed = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_:'
    if not isinstance(value, str) or not value or len(value) > 240 or any(c not in allowed for c in value):
        raise ValueError(f'{label} must be a nonempty provider identifier, not a URL or free text')
    if value.lower().startswith(('sk-', 'bearer', 'aiza', 'ghp_', 'ghs_', 'github_pat_')):
        raise ValueError(f'{label} looks like a credential; credentials must not be stored')
    return value


def stable_url(value):
    if not value:
        return ''
    # Signed downloads commonly carry credentials in the query. Stable project links do not need them.
    if not isinstance(value, str) or not value.startswith('https://') or any(c in value for c in '? #@\n\r\t'):
        raise ValueError('Use an HTTPS project link without query, fragment, credentials or whitespace')
    rest = value[len('https://'):]
    if not rest or not rest.split('/')[0] or any(c in rest for c in '\\'):
        raise ValueError('Invalid HTTPS project link')
    if any(piece in value.lower() for piece in ('/api/', '/download/', 'signature', 'access_token', 'credential')):
        raise ValueError('Use a stable editor/project link, not a download or API URL')
    return value


def jobs(project):
    data = read_json(project / 'provider-jobs.json')
    if not isinstance(data, dict) or set(data) != {'version', 'jobs'} or data['version'] != 1 or not isinstance(data['jobs'], list):
        raise ValueError('Invalid provider-jobs.json: expected version 1 and jobs list')
    seen = set()
    active = set()
    for job in data['jobs']:
        if not isinstance(job, dict) or set(job) != set(JOB_FIELDS):
            raise ValueError('A job must contain only provider, job_id, state, conversation_id and url; never credentials')
        if job['provider'] not in PROVIDERS or job['state'] not in STATES:
            raise ValueError('Unknown provider or job state')
        identifier(job['job_id'], 'Job ID')
        if job['conversation_id']:
            identifier(job['conversation_id'], 'Conversation ID')
        stable_url(job['url'])
        key = (job['provider'], job['job_id'])
        if key in seen:
            raise ValueError('Duplicate provider job ID in ledger')
        seen.add(key)
        if job['state'] in ACTIVE:
            if job['provider'] in active:
                raise ValueError('Multiple in-flight jobs for one provider; reconcile the ledger before continuing')
            active.add(job['provider'])
    return data


def load_project(project):
    project = Path(project).resolve()
    brief = read_json(project / 'brief.json')
    if not isinstance(brief, dict) or brief.get('track') not in TRACKS:
        raise ValueError('brief.json must be an object with track heuro or personal')
    shots = csv_rows(project / 'storyboard.csv', SHOT_FIELDS)
    assets = csv_rows(project / 'assets.csv', ASSET_FIELDS)
    return project, brief, shots, assets, jobs(project)


def init_project(slug, track, root=None):
    allowed = 'abcdefghijklmnopqrstuvwxyz0123456789-'
    if (not slug or len(slug) > 80 or slug[0] == '-' or slug[-1] == '-'
            or any(c not in allowed for c in slug)):
        raise ValueError('Slug must be 1–80 lowercase letters/digits with internal hyphens only')
    if track not in TRACKS:
        raise ValueError('Track must be heuro or personal')
    project = (Path(root) if root is not None else BASE / 'projects').resolve() / track / slug
    # mkdir rejects existing directories, files and symlinks instead of overwriting work.
    try:
        project.mkdir(parents=True, exist_ok=False)
    except FileExistsError as error:
        raise ValueError(f'Project already exists: {project}; choose a new slug') from error
    brief = {'version': 1, 'title': slug.replace('-', ' ').title(), 'track': track, 'status': 'draft',
             'audience': '', 'goal': '', 'language': '', 'platforms': [], 'duration_seconds': 30,
             'aspect_ratio': '9:16', 'message': '', 'cta': '', 'script': '', 'approved_claims': [],
             'references': [], 'avatar_id': None, 'voice_id': None, 'budget': None,
             'open_questions': []}
    write_json(project / 'brief.json', brief)
    write_csv(project / 'storyboard.csv', SHOT_FIELDS, [dict(zip(SHOT_FIELDS,
              ('1', '0', '5', 'speaking', '', '', '')))])
    write_csv(project / 'assets.csv', ASSET_FIELDS, [])
    write_json(project / 'provider-jobs.json', {'version': 1, 'jobs': []})
    return project


def get_context(context_dir=None, track='heuro'):
    path = Path(context_dir) if context_dir is not None else BASE / 'context'
    preferences = read_json(path / 'preferences.json', {})
    if not isinstance(preferences, dict):
        raise ValueError('preferences.json must be an object')
    confirmed = preferences.get('confirmed', {})
    unresolved = preferences.get('unresolved', {})
    if not isinstance(confirmed, dict) or not isinstance(unresolved, dict):
        raise ValueError('Preference confirmed/unresolved sections must be objects')
    filenames = ('persona.md',) if track == 'personal' else ('heuro.md', 'product-context.md')
    documents = []
    for filename in filenames:
        document = path / filename
        if document.exists():
            documents.append(f'### {filename}\n' + document.read_text(encoding='utf-8'))
    product = '\n\n'.join(documents)
    provenance = ('Provenance reference: source-register.json (use the sources cited by this track; '
                  'the full register is not copied into provider prompts).'
                  if (path / 'source-register.json').exists()
                  else 'Provenance reference: source-register.json not supplied; source links need verification.')
    product = (product + '\n\n' if product else 'No track-specific context supplied; do not invent background.\n\n') + provenance
    gaps = []
    if not (path / 'preferences.json').exists():
        gaps.append('No private preference profile loaded; personal style and identity remain unknown')
    if not documents:
        gaps.append('No track-specific persona context loaded' if track == 'personal' else 'No source-backed product context loaded')
    return confirmed, unresolved, product, gaps


def readiness(brief, shots, assets, ledger, context_dir=None):
    confirmed, unresolved, product, context_gaps = get_context(context_dir, brief['track'])
    missing = [field for field in ('title', 'audience', 'goal', 'language', 'message', 'cta', 'script') if not brief.get(field)]
    if not isinstance(brief.get('duration_seconds'), (int, float)) or isinstance(brief.get('duration_seconds'), bool) or not math.isfinite(brief['duration_seconds']) or brief['duration_seconds'] <= 0:
        missing.append('positive duration_seconds')
    if brief.get('aspect_ratio') not in ('9:16', '16:9', '1:1'):
        missing.append('supported aspect_ratio')
    shot_issues = []
    if not shots:
        shot_issues.append('Storyboard has no shots')
    total_end = 0
    intervals = []
    seen = set()
    routes = []
    for row in shots:
        shot_id = row['shot_id']
        if not shot_id or shot_id in seen:
            shot_issues.append('Shot IDs must be nonempty and unique')
        seen.add(shot_id)
        try:
            start = float(row['start_seconds']); duration = float(row['duration_seconds'])
            if not (math.isfinite(start) and math.isfinite(duration) and start >= 0 and duration > 0 and start < 86400 and duration < 86400):
                raise ValueError()
            total_end = max(total_end, start + duration)
            intervals.append((start, start + duration, shot_id))
        except ValueError:
            shot_issues.append(f'Shot {shot_id}: invalid start/duration')
        if row['kind'] not in ROUTES:
            shot_issues.append(f'Shot {shot_id}: unknown kind {row["kind"]!r}')
        if not row['visual'] and not row['narration']:
            shot_issues.append(f'Shot {shot_id}: narration or visual direction required')
        routes.append({'shot_id': shot_id, 'kind': row['kind'], 'provider': ROUTES.get(row['kind'], 'unresolved')})
    previous_end = 0.0
    for start, end, shot_id in sorted(intervals):
        if not math.isclose(start, previous_end, rel_tol=0, abs_tol=0.001):
            relation = 'gap' if start > previous_end else 'overlap'
            shot_issues.append(f'Shot {shot_id}: storyboard {relation} at {start:g}s (previous end {previous_end:g}s)')
        previous_end = max(previous_end, end)
    duration = brief.get('duration_seconds')
    if (isinstance(duration, (int, float)) and not isinstance(duration, bool)
            and math.isfinite(duration) and not math.isclose(total_end, duration, rel_tol=0, abs_tol=0.001)):
        shot_issues.append('Storyboard end does not match the brief duration')
    unresolved_assets = [row['asset_id'] or '(unnamed)' for row in assets
                         if row['status'] != 'ready' or not row['stable_storage_id'] or not row['rights']]
    warnings = list(context_gaps)
    if any(row['kind'] == 'speaking' for row in shots):
        if not brief.get('avatar_id') or not brief.get('voice_id'):
            warnings.append('Verify the own avatar and voice in the provider before generating speaking shots')
    if brief.get('budget') is None:
        warnings.append('No generation budget recorded')
    if not assets:
        warnings.append('No source/reference assets registered')
    warnings.append('Provider account readiness and output quality require live checks; this CLI has not tested them')
    running = [j for j in ledger['jobs'] if j['state'] in ACTIVE]
    return {'local_plan_complete': not missing and not shot_issues and not unresolved_assets,
            'provider_ready': False, 'missing_brief_fields': missing, 'storyboard_issues': shot_issues,
            'unresolved_assets': unresolved_assets, 'context_questions': sorted(unresolved),
            'warnings': warnings, 'routes': routes, 'in_flight_jobs': running,
            'next_action': 'Follow existing jobs; do not submit duplicates' if running else 'Complete local gaps, then verify provider access before generation'}


def project_status(project, context_dir=None):
    _, brief, shots, assets, ledger = load_project(project)
    return readiness(brief, shots, assets, ledger, context_dir)


def build_pack(project, context_dir=None):
    project, brief, shots, assets, ledger = load_project(project)
    confirmed, unresolved, product, _ = get_context(context_dir, brief['track'])
    status = readiness(brief, shots, assets, ledger, context_dir)
    generated = project / 'generated'
    generated.mkdir(exist_ok=True)
    identity = confirmed.get('synthesia_identity_name', '[own identity name unresolved]')
    # Render only selected profile values. Account configuration and credentials are never copied.
    profile = json.dumps(confirmed, indent=2, ensure_ascii=False)
    brief_text = json.dumps(brief, indent=2, ensure_ascii=False)
    common = ('This is a draft production brief, not permission to publish. Follow the user’s actual instructions.\n'
              'Unknown values must remain unknown. Do not invent claims, personal experiences or identity IDs.\n\n'
              f'## Brief\n{brief_text}\n\n## Confirmed preferences\n{profile}\n\n'
              f'## Track-specific context\n{product or "No track-specific context supplied; do not invent background."}\n\n')
    shot_text = '\n'.join(f"Shot {r['shot_id']} at {r['start_seconds']}s for {r['duration_seconds']}s [{r['kind']}]: "
                          f"Narration: {r['narration']}; visual: {r['visual']}; on-screen text: {r['on_screen_text']}" for r in shots)
    synthesia = (common + f'Use the user’s own identity named {identity!r}, after checking it in the connected account. '
                 f"Requested avatar ID: {brief.get('avatar_id') or 'unverified'}; voice ID: {brief.get('voice_id') or 'unverified'}. "
                 'Never substitute a stock character and present it as the user. Use the current Syren flow. '
                 'Reuse an existing conversation handle for revisions and record it in the job ledger. '
                 'Handle native provider clarification if identity selection is unresolved.\n\n' + shot_text)
    google = (common + 'Generate only illustrative scene shots from the storyboard. Preserve approved references and character continuity. '
              'Check current model availability and account access; no model/version is assumed here. '
              'Create exact text, data graphics and UI in an editor instead. Record model/version and take selection. '
              'Illustrative sites must not be passed off as surveyed real parcels.\n\n' + shot_text)
    descript = (common + 'Import the selected generated and supplied clips into the requested composition. '
                'Assemble to the storyboard; edit pacing, captions and dialogue/music balance. '
                'Preserve the supplied script, actual UI, voice and identity. Review proper names and subtitle timing. '
                'Do not publish unless authorized by the user. Retain the editing conversation ID for revisions.\n\n' + shot_text)
    for name, prompt in (('synthesia.md', synthesia), ('google-scenes.md', google), ('descript-edit.md', descript)):
        (generated / name).write_text(prompt + '\n', encoding='utf-8')
    text = ('# Production pack\n\nGenerated locally. No provider jobs were submitted. Generated files may contain private context; '
            'keep them out of public Git. Regenerating this folder replaces its files; keep accepted edits in the brief/storyboard.\n\n'
            + common + '## Storyboard\n' + shot_text + '\n\n## Routing and gaps\n'
            + json.dumps(status, indent=2, ensure_ascii=False)
            + '\n\n## Deliverables\nMaster and platform exports, captions, thumbnail, asset provenance and full-playback review.\n')
    (generated / 'production.md').write_text(text + '\n', encoding='utf-8')
    return generated


def record_job(project, provider, job_id, state, conversation_id=None, url=None):
    project, _, _, _, ledger = load_project(project)
    if provider not in PROVIDERS or state not in STATES:
        raise ValueError('Unknown provider or state')
    identifier(job_id, 'Job ID')
    if conversation_id is not None and conversation_id:
        identifier(conversation_id, 'Conversation ID')
    if url is not None:
        stable_url(url)
    existing = next((j for j in ledger['jobs'] if j['provider'] == provider and j['job_id'] == job_id), None)
    if any(j['provider'] == provider and j['job_id'] != job_id and j['state'] in ACTIVE for j in ledger['jobs']):
        raise ValueError('This provider already has an in-flight job; follow or resolve it before recording another')
    if existing is None:
        existing = {'provider': provider, 'job_id': job_id, 'state': state, 'conversation_id': '', 'url': ''}
        ledger['jobs'].append(existing)
    existing['state'] = state
    if conversation_id is not None:
        existing['conversation_id'] = conversation_id
    if url is not None:
        existing['url'] = url
    write_json(project / 'provider-jobs.json', ledger)
    return existing


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    create = sub.add_parser('init', help='Create a project without overwriting existing work')
    create.add_argument('slug'); create.add_argument('--track', choices=TRACKS, required=True)
    create.add_argument('--root', type=Path, help='Projects parent directory; default videos/projects')
    for name in ('pack', 'status'):
        cmd = sub.add_parser(name)
        cmd.add_argument('project', type=Path)
        cmd.add_argument('--context', type=Path, help='Context directory; default videos/context')
    record = sub.add_parser('record-job', help='Record/update an existing provider job; never submits a job')
    record.add_argument('project', type=Path)
    record.add_argument('--provider', choices=PROVIDERS, required=True)
    record.add_argument('--job-id', required=True)
    record.add_argument('--state', choices=STATES, required=True)
    record.add_argument('--conversation-id'); record.add_argument('--url')
    args = parser.parse_args(argv)
    try:
        if args.command == 'init':
            print(init_project(args.slug, args.track, args.root))
        elif args.command == 'pack':
            print(build_pack(args.project, args.context))
        elif args.command == 'status':
            print(json.dumps(project_status(args.project, args.context), indent=2, ensure_ascii=False))
        else:
            print(json.dumps(record_job(args.project, args.provider, args.job_id, args.state,
                                        args.conversation_id, args.url), indent=2))
    except (ValueError, OSError) as error:
        parser.error(str(error))
    return 0


if __name__ == '__main__':
    sys.exit(main())
