# Video production research

Researched **2026-11-05** from publisher repositories and official documentation. The [machine-readable catalog](capability-catalog.json) now contains **45 tools, services and skill sources**: 29 baseline entries plus 16 launch-film additions. See [the launch-film extension](launch-film-stack.md) and [acquired skills](skill-acquisition.md) for the latest setup status and additional revision pins. This is a curated lifecycle inventory, not a claim to index every tool or to rank untested models by quality. It contains generic research only; account readiness and personal context belong in private configuration.

## Recommended working stack

Use the smallest stack that covers the job. Start with the existing authorized avatar provider, one generated-scene provider, one editing surface and deterministic media utilities. Add an open-model GPU workflow when a controlled test shows a useful benefit.

| Need | Starting choice | Alternative / boundary |
|---|---|---|
| Own speaking character | [Synthesia](https://docs.synthesia.io/) | [HeyGen](https://developers.heygen.com/) as a comparison if the existing avatar disappoints |
| Cinematic short scenes | [Google Flow](https://support.google.com/flow/) or [current Google video API](https://aistudio.google.com/docs/video) | [Runway](https://docs.dev.runwayml.com/); test the same representative shot |
| Exact titles, captions, branding, map/UI animation | [Remotion](https://github.com/remotion-dev/remotion) | [Blender](https://github.com/blender/blender) for advanced 3D and compositing |
| Transcript-led editing, cleanup and clips | [Descript / Underlord](https://www.descript.com/underlord) | [Shotcut](https://github.com/mltframework/shotcut) for desktop finishing |
| Encode, resize, audio mix, packaging | [FFmpeg](https://github.com/FFmpeg/FFmpeg) | Current project already has a validated local export utility |
| Transcription | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | [WhisperX](https://github.com/m-bain/whisperX) when word alignment/diarization is required |
| Longer footage segmentation | [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | Editorial judgement still selects useful cuts |
| Controlled open-model generation | [ComfyUI](https://github.com/Comfy-Org/ComfyUI) + [Wan2.2](https://github.com/Wan-Video/Wan2.2) or [LTX-2 family](https://github.com/Lightricks/LTX-2) | [HunyuanVideo-1.5](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5) as another measured alternative |
| Lip-sync experiment | [MuseTalk](https://github.com/TMElyralab/MuseTalk) | Existing authorized own-avatar workflow remains simpler |
| Separate voice/dubbing service | [ElevenLabs](https://elevenlabs.io/docs/overview/intro) | Compare pronunciation and own-voice quality before adopting another account |
| Editor interchange | [OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO) | Test adapter fidelity; a timeline does not embed every font/effect/media file |
| Accurate map scenes | [MapLibre GL JS](https://github.com/maplibre/maplibre-gl-js) | Imagery, tiles and parcel data need their own provenance |
| Image cutouts | [rembg](https://github.com/danielgatis/rembg) | Review segmentation-model terms separately |
| Encode quality comparison | [VMAF](https://github.com/Netflix/vmaf) | Metrics do not evaluate storytelling, identity or factual accuracy |
| Private media transport | [rclone](https://rclone.org/overview/) + chosen Drive/S3 destination | Keep tokens outside Git and record stable file IDs/checksums |

Readiness is not inferred from a listing. FFmpeg was previously validated in this environment. The other repositories in this catalog were researched, not installed or benchmarked. An exposed connector does not by itself prove a paid feature, an approved avatar, API billing or an authenticated browser session.

## Official skills and agent interfaces

The [official Remotion skill source](https://github.com/remotion-dev/skills) currently documents: `remotion-best-practices`, `remotion-create`, `remotion-markup`, `remotion-studio`, `remotion-render`, `remotion-maps`, `remotion-captions`, `remotion-saas`, `remotion-interactivity`, `remotion-docs`, `remotion-license`, `remotion-upgrade` and `remotion-multimedia`. The [publisher's guide](https://www.remotion.dev/docs/ai/skills) explains installation. The repository has no GitHub-detected root licence; resolve the relationship to the upstream Remotion package before vendoring it. No upstream files were copied here.

Use available connected Descript skills for project creation, editing, transcript export, timeline export and publishing when the corresponding operation is requested. Synthesia's current connected Syren flow supplies creation/revision/status/export actions; it should not be replaced with a guessed API wrapper. Provider MCP/CLI availability advertised by [Runway](https://docs.dev.runwayml.com/) or [HeyGen](https://developers.heygen.com/) is a discovery option, not evidence that either account is connected.

## Model and licence findings that affect selection

- **Wan2.2:** repository metadata and [official README](https://github.com/Wan-Video/Wan2.2/blob/main/README.md) identify Apache-2.0, including a declaration for its models. The TI2V-5B example documents at least 24GB VRAM; an A14B example requires at least 80GB. These examples apply to their settings, not every resolution/precision/workflow.
- **LTX:** [code is Apache-2.0](https://github.com/Lightricks/LTX-2), while current 2.3 and 2.5 weights have distinct custom community licences. Do not describe the complete stack as Apache-licensed just because GitHub detects Apache for the repository.
- **HunyuanVideo-1.5:** uses [Tencent's custom licence](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5/blob/main/LICENSE). Its [README](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5/blob/main/README.md) documents 14GB minimum with model offloading; throughput and actual configuration still need testing.
- **MuseTalk:** the [README](https://github.com/TMElyralab/MuseTalk/blob/main/README.md) states MIT code and permits its trained model commercially, but companion models retain separate terms and sample test data is research-only. Use authorized source footage.
- **F5-TTS:** [MIT code and CC-BY-NC pretrained models](https://github.com/SWivid/F5-TTS/blob/main/README.md) are different. Exclude those supplied pretrained weights from the commercial promotional-video default.
- **Fish Speech:** its [current README](https://github.com/fishaudio/fish-speech/blob/main/README.md) distinguishes Fish Audio Community licensing from S2-Pro Research licensing. Select and review the precise checkpoint.
- **Remotion:** [custom free/company tiers](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md) depend on entity eligibility. It is not interchangeable with an MIT library. FFmpeg's deployed licence obligations likewise depend on its build and linked components.

The [official Google video documentation](https://aistudio.google.com/docs/video) currently states Veo 3.1 Preview retired on 2026-10-22 and points to current Gemini Omni Flash or a GA enterprise Veo route. Do not hard-code old preview identifiers; Flow product availability is a separate check.

## Reproducibility and selection

Pinned research snapshots: [Remotion skills a2824c6](https://github.com/remotion-dev/skills/commit/a2824c67f8b4585c294a8101db9f9f0ad3c643f8), [Wan 1ea34ff](https://github.com/Wan-Video/Wan2.2/commit/1ea34ff48f87168174e12956e200b1d908b1c5ff), [LTX 4f52161](https://github.com/Lightricks/LTX-2/commit/4f521619ae0029e8fbb64d555030c2b121a33b4f), [Hunyuan 60783e7](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5/commit/60783e704160023913bee78f0b47036d393d4dfa), [ComfyUI fb2b26f](https://github.com/Comfy-Org/ComfyUI/commit/fb2b26fdac507b7da81277c7becaf54c5e46ac6b). They are observation anchors, not installed versions.

Compare candidates on one short own-avatar shot, one controlled cinematic shot, one exact UI/map scene and one multilingual caption sample. Record model/checkpoint, prompt, references, seed where supported, first usable output time, actual spend and rejection reason. Score identity continuity, mouth sync, pronunciation, temporal stability, camera control, text accuracy, brand fit, editability and cost per usable second. Keep the best route per task, then preserve it in the production profile. A technically valid export still needs full human playback and factual review.
