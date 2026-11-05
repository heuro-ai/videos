#!/usr/bin/env python3
"""Assemble a local JSON video timeline with FFmpeg; never calls a provider."""
import argparse
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


FORMATS = {'vertical': (1080, 1920), 'landscape': (1920, 1080), 'square': (1080, 1080)}


def run(command):
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode:
        raise ValueError(f'{command[0]} failed: {result.stderr[-1800:].strip()}')
    return result.stdout


def number(value, label, minimum=0, maximum=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f'{label} must be a number')
    if not math.isfinite(value) or value < minimum or (maximum is not None and value > maximum):
        raise ValueError(f'{label} is outside the permitted range')
    return value


def local_file(value, base):
    if not isinstance(value, str) or not value or '://' in value:
        raise ValueError('Media references must be local file paths')
    path = Path(value).expanduser()
    path = (base / path).resolve() if not path.is_absolute() else path.resolve()
    if not path.is_file():
        raise ValueError(f'Media file does not exist: {path}')
    return path


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-protocol_whitelist', 'file,pipe',
                           '-show_streams', '-show_format', '-of', 'json', str(path)]))


def validate(path):
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError('Timeline must be a JSON object')
    style = data.get('format', 'vertical')
    if not isinstance(style, str) or style not in FORMATS:
        raise ValueError('format must be vertical, landscape or square')
    fps = number(data.get('fps', 30), 'fps', 1, 60)
    clips = data.get('clips')
    if not isinstance(clips, list) or not clips:
        raise ValueError('clips must be a nonempty list')
    ready = []
    for index, clip in enumerate(clips):
        if not isinstance(clip, dict):
            raise ValueError(f'Clip {index + 1} must be an object')
        media = local_file(clip.get('file'), path.parent)
        start = number(clip.get('start', 0), f'Clip {index + 1} start')
        duration = number(clip.get('duration'), f'Clip {index + 1} duration', 1 / fps)
        info = probe(media)
        videos = [stream for stream in info['streams'] if stream.get('codec_type') == 'video']
        if not videos:
            raise ValueError(f'Clip {index + 1} has no video stream')
        source_duration = videos[0].get('duration') or info.get('format', {}).get('duration')
        try:
            source_duration = float(source_duration)
        except (TypeError, ValueError):
            raise ValueError(f'Clip {index + 1}: cannot determine video duration') from None
        if not math.isfinite(source_duration) or start >= source_duration or start + duration > source_duration + 0.002:
            raise ValueError(f'Clip {index + 1} extends beyond its video source')
        frames = round(duration * fps)
        if abs(frames / fps - duration) > 0.00001:
            raise ValueError(f'Clip {index + 1} duration must span a whole number of output frames')
        ready.append({'file': media, 'start': start, 'duration': duration,
                      'audio': any(s.get('codec_type') == 'audio' for s in info['streams'])})
    voiceover = None
    if data.get('voiceover') is not None:
        voiceover = local_file(data['voiceover'], path.parent)
        if not any(s.get('codec_type') == 'audio' for s in probe(voiceover)['streams']):
            raise ValueError('voiceover has no audio stream')
    return style, fps, ready, voiceover


def assemble(timeline, output, check=False):
    if not all(shutil.which(name) for name in ('ffmpeg', 'ffprobe')):
        raise ValueError('Install ffmpeg and ffprobe first')
    if output.suffix.lower() != '.mp4':
        raise ValueError('Output must end with .mp4')
    if output.exists():
        raise ValueError('Output already exists; choose a new filename')
    style, fps, clips, voiceover = validate(timeline)
    width, height = FORMATS[style]
    total = sum(clip['duration'] for clip in clips)
    summary = {'clips': len(clips), 'width': width, 'height': height, 'fps': fps,
               'duration_seconds': round(total, 6), 'audio': 'voiceover' if voiceover else 'clip audio / silence'}
    if check:
        return dict(summary, validated=True, rendered=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.video-assemble-', dir=output.parent) as work:
        work = Path(work)
        for index, clip in enumerate(clips):
            duration = str(clip['duration'])
            command = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-n',
                       '-protocol_whitelist', 'file,pipe', '-ss', str(clip['start']), '-i', str(clip['file'])]
            if not clip['audio']:
                command += ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo']
            command += ['-map', '0:v:0', '-map', '0:a:0' if clip['audio'] else '1:a:0',
                        '-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,'
                               f'pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,'
                               f'fps={fps},tpad=stop_mode=clone:stop_duration={duration}',
                        '-af', f'apad,atrim=duration={duration},asetpts=PTS-STARTPTS',
                        '-t', duration, '-c:v', 'libx264', '-threads', '2', '-preset', 'veryfast',
                        '-crf', '18', '-pix_fmt', 'yuv420p', '-video_track_timescale', '90000',
                        '-c:a', 'aac', '-ar', '48000', '-ac', '2', '-b:a', '192k',
                        str(work / f'clip-{index}.mp4')]
            run(command)
        concat = work / 'clips.txt'
        concat.write_text(''.join(f"file 'clip-{i}.mp4'\n" for i in range(len(clips))))
        joined = work / 'joined.mp4'
        run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-n', '-f', 'concat', '-safe', '1',
             '-i', str(concat), '-map', '0:v:0', '-map', '0:a:0', '-c', 'copy',
             '-movflags', '+faststart', str(joined)])
        final = joined
        if voiceover:
            final = work / 'narrated.mp4'
            run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-n', '-i', str(joined),
                 '-protocol_whitelist', 'file,pipe', '-i', str(voiceover),
                 '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy',
                 '-af', f'apad,atrim=duration={total},asetpts=PTS-STARTPTS', '-t', str(total),
                 '-c:a', 'aac', '-ar', '48000', '-ac', '2', '-b:a', '192k',
                 '-movflags', '+faststart', str(final)])
        # Exclusive hard link publishes a complete file without clobbering a concurrent output.
        os.link(final, output)
    return dict(summary, output=str(output), rendered=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('timeline', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--check', action='store_true', help='Validate all inputs without rendering')
    args = parser.parse_args()
    try:
        print(json.dumps(assemble(args.timeline.resolve(), args.output.resolve(), args.check), indent=2))
    except (ValueError, OSError, KeyError) as error:
        print(f'Assembly failed: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
