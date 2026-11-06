# Official video skills acquired

Checked 2026-11-06. The first-party [Remotion skills repository](https://github.com/remotion-dev/skills) has been fetched into the ignored `vendor/agent-skills/remotion-skills/` directory and checked out at **a2824c67f8b4585c294a8101db9f9f0ad3c643f8**, dated 2026-11-05. Its package and skill metadata report **4.0.541**. [Remotion’s own documentation](https://www.remotion.dev/docs/ai/skills) identifies this repository as its agent guidance. `skill-lock.json` records the checkout, inventory, read files, hashes and immutable source links.

This is an actual reviewed checkout, not just a list of recommendations. No package installer or lifecycle script was run by this acquisition step, and it is not registered as a global agent skill. A runtime still needs its own compatible packages, browser and working preview/render check.

## Read before building a starter

All paths below are relative to `vendor/agent-skills/remotion-skills/`. Open the actual files, rather than treating this summary as a replacement for their instructions.

| Task | Read these files |
|---|---|
| Route a Remotion task | `skills/remotion-best-practices/SKILL.md` |
| New project/composition | `skills/remotion-create/SKILL.md`, then `skills/remotion-create/video-layout.md` |
| Register compositions | `skills/remotion-markup/SKILL.md`, then `skills/remotion-markup/compositions.md` |
| Timing and multi-scene motion | `skills/remotion-markup/timing.md`, `sequencing.md`, `multi-scene-video.md`, `transitions.md` |
| Render or extract frames | `skills/remotion-render/SKILL.md` |
| Geographic imagery | `skills/remotion-maps/SKILL.md`, then exactly the technique selected for the shot |
| Static map plate | `skills/remotion-maps/techniques/static-map/TECHNIQUE.md` |
| MapLibre animation | `skills/remotion-maps/techniques/maplibre/TECHNIQUE.md`; moving cameras additionally require its `references/render-stability.md` |
| Captions | `skills/remotion-captions/SKILL.md`, then `display-captions.md` or `import-srt-captions.md` as appropriate |
| Motion blur | `skills/remotion-markup/motion-blur.md` |
| Licensing | `skills/remotion-license/SKILL.md` and the current official licence/FAQ/terms pages |

The inventory also includes skills for Studio, API documentation, interactivity, multimedia, SaaS architecture and upgrades. They are fetched but not all were read during this focused acquisition.

## Instructions that affect implementation

The create/router guidance prioritizes opening Studio early so the user can steer. It treats a preview as the default output and asks for explicit export/render intent before a full render; existing user authorization takes precedence. The render guidance requires Remotion’s bundled browser rather than repurposing an automation browser. Do not claim a preview opened when no browser was available.

The markup guidance uses frame-driven motion, `interpolate()` and video `fps` for timing. Browser-timed CSS transitions/animations are unsuitable for deterministic rendering. Keep frame subscriptions local to the smallest animated components. Inline editable composition metadata/defaults and authored scene nodes preserve Studio editing. Current media guidance uses `@remotion/media`; exact package/API compatibility must be checked for the installed version. Resolve package versions together rather than mixing unrelated releases.

For multi-scene launch films, choose an authored scene structure before layering effects. Adjacent scenes and their transitions must account for overlap: a crossfade consumes frames from both scenes, so the master duration is shorter than the simple sum. Title, supporting text and core action need intentional hierarchy and generous frame-safe margins. Avoid treating the composition as a webpage.

Maps need the least complicated technique that explains the shot. A licensed static map plate with deterministic overlays is often sufficient. MapLibre adds reusable route/marker animation, but map data and style/tile terms remain separate from the open map renderer. Keep attribution visible. The reviewed MapLibre instructions require explicit load/frame synchronization and advise checking an actual short render for shimmer before a moving map camera. This technique does not create genuine 3D terrain; inspect its stability reference before using that approach.

Captions use the typed JSON caption format with millisecond timestamps. Keep caption timing with its corresponding clip, including shared trim/speed changes. The display skill links to a first-party Basic Captions element source; that external source was **not** copied or reviewed during this acquisition. Load it before choosing that implementation, and preserve the distinction between manually supplied caption text and speech that was genuinely transcribed.

Optional motion blur has browser/API prerequisites and additional render cost. Use it only when a shot needs it and the runtime supports it. Adding a skill does not guarantee the aesthetic quality of a video; actual source assets, direction, edit rhythm, sound and review still determine the result.

## Licensing and distribution

No `LICENSE`, `COPYING` or `NOTICE` file was found in the pinned standalone skills repository. The checkout remains under ignored `vendor/`; only this original guide and metadata manifest should be tracked. Public source access does not establish a right to republish all source files.

Remotion’s [licence FAQ](https://www.remotion.dev/docs/license/faq) identifies the software as source-available rather than OSI open source. It describes free eligibility for individuals and small organizations, and company licensing where that eligibility does not apply. This project does not establish the operator’s organizational headcount or legal eligibility. Check [the licence](https://www.remotion.dev/docs/license) and [terms](https://www.remotion.dev/docs/terms) for the actual commercial setup; no paid purchase was made here. Source-reading and a local prototype can continue while keeping commercial eligibility explicit.

## Reproduce or refresh

From `videos/`, fetch the official repository into a new ignored vendor checkout, then select the exact commit from `research/skill-lock.json`:

```sh
git clone https://github.com/remotion-dev/skills.git vendor/agent-skills/remotion-skills
git -C vendor/agent-skills/remotion-skills checkout --detach a2824c67f8b4585c294a8101db9f9f0ad3c643f8
```

Do not run this over a checkout containing local changes. A refresh should review changes, update the commit and file hashes, and check guidance against the runtime package versions. The initial checkout targets directly relevant video guidance. The additional first-party Motion kit below supports UI animation work; generic marketplace bundles were not added merely to increase the count.

## Additional first-party acquisition: Motion AI Kit

The official [Motion AI Kit repository](https://github.com/motiondivision/ai-kit) is also fetched under ignored `vendor/agent-skills/motion-ai-kit/`, pinned to **1e424943582cbbdb6e3f410687e39f96451447bb**, dated 2026-10-26. Its installer package metadata reports **14.2.0**; this is not the version of an installed Motion runtime. The checkout contains a real standalone `/motion` skill at `plugins/motion/skills/motion/SKILL.md`, supported by local best-practice files and documentation for hosted MCP capabilities. It is more than a CLI README, but fetching it does not automatically connect its servers or register its skill.

The skill, React guidance, CSS-versus-Motion decision guide, documentation-search instructions, installer metadata and public MCP configuration have been read. Local best-practice guidance is immediately readable without a server. Search, easing generation and advanced interactive capabilities require the relevant MCP connection. **No `npx motion-ai` installer was run, no `.codex/config.toml` or global settings were changed, and no Motion+ entitlement was assumed.** The manifest distinguishes acquired local files from setup merely described upstream.

For the UI surrounding a video tool, read the Motion skill and `best-practices/index.md`, `css-or-motion.md`, `react.md` first. The [official setup guide](https://motion.dev/docs/ai-kit) explains supported agent installation, including Codex. Optional Motion+ source and audit features need their own sign-in and entitlement; gated source was not reconstructed or copied. Motion’s own package README and package metadata declare MIT, but the pinned tree contains no separate LICENSE file; the source remains in ignored vendor storage.

This kit is **web/UI animation guidance**, not a drop-in replacement for Remotion’s frame-driven video timeline. Its browser-timed Motion/CSS animation recipes should not be placed into an offline video composition when Remotion requires deterministic frame-based motion. Use the Remotion instructions above for the rendered video and Motion guidance where an actual interactive UI needs it.

There are now **14 acquired standalone skills across two pinned first-party repositories**: 13 Remotion skills and one Motion skill. This counts files acquired, not 14 installed or connected services. Package scripts, paid dependencies, hosted services and model weights remain separate readiness checks.

## Verify or reproduce with the project command

From videos/, run `python3 scripts/skill_sources.py` to verify local revisions and reviewed-file hashes. On another environment, `python3 scripts/skill_sources.py --fetch` retrieves absent pinned repositories without running installers or changing global skill/MCP configuration. Existing changed checkouts are left unchanged.
