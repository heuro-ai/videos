# Launch-film stack: real demos, spatial UI and restrained motion

Research date: **2026-11-06**. This adds **16 incremental entries** to the existing 29-entry catalog; it does not repeat Remotion, FFmpeg, MapLibre, Blender or the existing avatar/editor choices as new discoveries. Eight upstream revisions are recorded in [launch-film-stack.json](launch-film-stack.json). All new entries are **researched, not installed by this task**.

## Small core to build first

Use **real product capture → frame-controlled composition → approved founder segments → sound mix and finishing**. This is a proposed production architecture, not a claim that one tool universally produces the best-looking film.

1. **Record an actual working demo.** [Playwright](https://playwright.dev/docs/videos) can repeat browser actions and record their result. Set matching viewport and video dimensions explicitly; its default may scale recordings down. Use a demo account and authorized test data, close the context to finish writing the video, and preserve the capture script with the take.
2. **Compose the narrative in the existing Remotion path.** Build a short set of typography, spacing, timing and easing tokens. Reveal the product benefit, then show the actual behaviour that demonstrates it. Keep the UI readable before introducing any spatial treatment.
3. **Add depth only where it explains something.** [Three.js](https://threejs.org/docs/) with [React Three Fiber](https://r3f.docs.pmnd.rs/getting-started/introduction) and selected [Drei helpers](https://github.com/pmndrs/drei) can create a restrained spatial panel system. [Remotion's Three integration](https://www.remotion.dev/docs/three) supplies frame-aware scene integration and video textures; its [official minimal template](https://github.com/remotion-dev/template-three) is a concrete starting reference.
4. **Integrate the founder deliberately.** Use an approved real recording or the established own-avatar route for the opening thesis or a natural closing thought. Preserve clean dialogue separately from music and FX so edits can improve pacing without regenerating the whole film.
5. **Finish against one master specification.** Use the existing editor/FFmpeg route for standard delivery. Add [Resolve/Fairlight/Fusion](https://www.blackmagicdesign.com/products/davinciresolve) when final grade, complex composites or a detailed sound mix warrant a specialist desktop pass.

## Real capture alternatives

[OBS Studio](https://github.com/obsproject/obs-studio) is the open recording alternative for camera, desktop and audio capture. A working desktop, capture permissions and encoder still need setup. [Screen Studio](https://screen.studio/) is an optional macOS route for fast cursor/zoom/framing polish; no supported cloud API or CLI was established here. Choose one capture route per job rather than adding all three.

Real demo means recorded behaviour of the real product. A plausible generative UI is not evidence that a feature exists. Use a labelled prototype when an unbuilt feature must be presented as a concept. Keep any personal information and capture credentials out of the repository.

## Spatial and motion options

| Need | Incremental option | Use boundary |
|---|---|---|
| Precise 3D panels, camera and lighting | Three.js + R3F + selected Drei helpers | Render from composition frame/time, not an uncontrolled animation clock |
| Dense geospatial evidence overlays | [deck.gl](https://deck.gl/docs) over the existing MapLibre path | Dataset, tile and imagery terms are separate from MIT code |
| Terrain/globe/3D tiles | [CesiumJS](https://cesium.com/learn/cesiumjs-learn/cesiumjs-quickstart/) | Apache-2.0 library does not include rights to every ion service or terrain/imagery asset |
| React UI/layout motion | [Motion](https://motion.dev/docs/react) | MIT core; optional paid content is separate; final video needs deterministic timing |
| Complex SVG/stagger/timeline motion | [GSAP](https://gsap.com/standard-license/) | Custom licence covers commercial use free but restricts competing visual animation builders |
| Specialist visual keyframing | [Theatre.js](https://github.com/theatre-js/theatre) | Core Apache-2.0, studio AGPL-3.0; public maintenance signal is old, so keep experimental |
| Designer vector-motion handoff | [Lottie Web](https://github.com/airbnb/lottie-web) | MIT runtime; confirm which effects survive export and preserve original source |
| Bespoke designer-led compositing | [After Effects](https://www.adobe.com/products/aftereffects.html) | Proprietary optional desktop path; verify licence, fonts and plugin dependencies |

Motion's [official AI Kit](https://github.com/motiondivision/ai-kit) documents a `/motion` skill and free documentation MCP, including Codex setup via `npx motion-ai`. Motion+ audits/example source are a separate paid capability. The [Motion README](https://github.com/motiondivision/motion/blob/main/README.md) calls the skill MIT, while GitHub detects no licence for the whole AI Kit repository. Review the installer and relevant files before installation or vendoring; none was run here.

## Practical quality gates

These are production recommendations inferred from the tool capabilities:

- Script the argument before designing effects: tension → insight → actual demonstration → consequence → one next action.
- Preserve a clean source recording; camera moves and callouts are separate edit layers.
- Keep text stable long enough to read; use a limited easing and transition vocabulary.
- Start every spatial shot with a readable screen, then use perspective/lighting to guide attention.
- Use music and sound accents to support the story, while preserving intelligible dialogue and quiet moments.
- Review a full-resolution still, a phone preview, transitions at frame boundaries and the entire sound mix.
- Record capture provenance, source commit/build where available, asset rights, edit settings and delivery specs.

Software breadth does not substitute for art direction or a strong real demo. Start with the small core, produce one representative sequence, and add advanced tools only for an identified shot or finishing need.
