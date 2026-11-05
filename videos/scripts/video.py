#!/usr/bin/env python3
"""Small local media utilities; no provider credentials or network calls."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('doctor')
    probe = sub.add_parser('probe')
    probe.add_argument('input', type=Path)
    export = sub.add_parser('export')
    export.add_argument('input', type=Path)
    export.add_argument('output', type=Path)
    export.add_argument('--format', choices=['vertical', 'landscape', 'square'], default='vertical')
    args = parser.parse_args()
    if args.command == 'doctor':
        state = {tool: bool(shutil.which(tool)) for tool in ['ffmpeg', 'ffprobe']}
        print(json.dumps(state, indent=2))
        return 0 if all(state.values()) else 1
    if not args.input.is_file():
        parser.error('Input file does not exist')
    if args.command == 'probe':
        return subprocess.run(['ffprobe', '-v', 'error', '-show_format', '-show_streams',
                               '-of', 'json', str(args.input.resolve())], check=False).returncode
    if args.output.exists():
        parser.error('Output already exists; choose a new filename')
    if args.output.suffix.lower() != '.mp4':
        parser.error('Export output must end with .mp4')
    width, height = {'vertical': (1080, 1920), 'landscape': (1920, 1080), 'square': (1080, 1080)}[args.format]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    filters = (f'scale={width}:{height}:force_original_aspect_ratio=decrease,'
               f'pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30')
    result = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-n',
                             '-i', str(args.input.resolve()), '-map', '0:v:0', '-map', '0:a:0?',
                             '-vf', filters, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                             '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                             '-movflags', '+faststart', str(args.output.resolve())], check=False)
    if result.returncode:
        print('Export failed; inspect any partial output before retrying.', file=sys.stderr)
    return result.returncode


if __name__ == '__main__':
    try:
        sys.exit(main())
    except FileNotFoundError as error:
        print(f'Required executable is unavailable: {error.filename}', file=sys.stderr)
        sys.exit(1)
