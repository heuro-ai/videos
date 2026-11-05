# Assemble local footage

`scripts/assemble.py` turns an ordered JSON timeline into an MP4 using the installed FFmpeg and ffprobe. It runs locally on CPU, supports hard cuts, preserves the full frame with letterboxing, and normalizes each shot to H.264/AAC with stereo 48 kHz audio. Clips without audio receive silence. It does not generate footage or perform creative review.

```json
{
  "format": "vertical",
  "fps": 30,
  "clips": [
    {"file": "footage/opening.mp4", "start": 0, "duration": 3},
    {"file": "footage/detail.mp4", "start": 1, "duration": 5}
  ],
  "voiceover": "audio/narration.wav"
}
```

Media paths resolve relative to the timeline JSON. Absolute local paths also work. `format` accepts `vertical` (1080×1920), `landscape` (1920×1080) or `square` (1080×1080). `fps` is between 1 and 60. Each clip duration must span a whole number of output frames and fit inside its source video. Omit `voiceover` to retain each clip's audio; supplying it replaces all clip audio with narration, trimmed or padded with silence to the timeline length.

```sh
python3 scripts/assemble.py timeline.json exports/master.mp4 --check
python3 scripts/assemble.py timeline.json exports/master.mp4
```

The utility validates every source and narration file before rendering. It refuses existing output paths and publishes a complete MP4 only after all processing succeeds. Temporary encoded clips are removed on completion or failure. Rendering can require substantial temporary disk space; the output directory must be on a filesystem supporting hard links.

Captions, music mixing, transitions, face-aware crops and colour matching remain editor tasks. Concatenation copies normalized segments, so container/audio timestamps can differ from the requested duration by a small fraction of a second. Review the complete export and use ffprobe to verify actual duration, dimensions and audio before delivery.
