# Production workflow

This workflow is operated by an assistant with connected tools. The local CLI prepares briefs, prompts and a job ledger; it does not log into provider accounts or automatically invoke them.

## One-time setup

Record confirmed audience, language, reference links, character/voice, pronunciation, wardrobe, background, captions and spending preferences in private context. Store unknowns explicitly. A named avatar is not an observed avatar ID. Keep context portable so each future assistant can read it before writing a script.

Maintain a small approved asset library in private media storage: portrait references, avatar/provider IDs, a voice reference, pronunciation samples, brand logos/type/colors, product captures, rights information and example videos. Record stable storage IDs and checksums; expiring download URLs are transport only.

## Per video

1. Create a project with a clear track, audience, message, platform and desired action. Reuse confirmed defaults; ask only about material gaps.
2. Load the persona, product facts, preferences and reference analysis. Identify which claims are established, which are proposals and which need current evidence.
3. Write three hooks, choose the strongest for the brief, then draft one timed script and storyboard. Specify visual evidence, narration, graphics, audio and shot duration separately.
4. Create a short identity/style test when the character or aesthetic changes. Preserve references and pronunciation. Select the provider by the shot, using the capability catalog.
5. Produce assets and record provider job/conversation IDs immediately. Resume existing jobs; never resubmit because a wait timed out. Keep rejected takes with reasons until the final is selected.
6. Assemble and edit. Use real captures for product UI and actual site evidence. Generated maps, aerials and interfaces are illustrative assets, not proof. Add exact typography and labels during composition.
7. Mix speech, music and sound effects. Correct captions against speech; check proper names and language switching. Create deliberate reframes for each aspect ratio.
8. Watch the whole result and review representative frames, mouth sync, transitions, factual accuracy and phone readability. A successful encoding command proves only technical rendering.
9. Deliver a master, platform variants, subtitle file, thumbnail, script, asset manifest and project/timeline links as requested. Move final files to durable private media storage and record checksums.
10. Publish only under the user's actual authorization. Capture useful feedback as dated preferences. Record costs actually returned by providers; do not invent estimates or quotas.

## Batch production

Batch ideation and scripting, then generation and editing. Choose the mix of product videos, personal reels, demonstrations and timely commentary from the creator’s actual goals and confirmed capacity.

## Failure recovery

| Situation | Action |
|---|---|
| A provider job is still running | Poll its existing ID; keep the progress and resumable handle |
| Personal avatar is unavailable | Resolve the account/selection; do not silently use a stock identity |
| Generated text/UI is wrong | Composite accurate text or use a real product capture |
| A scene looks good but changes identity | Reject that take; reuse the approved references or avatar |
| Google UI access works but API access does not | Treat them as separate integrations; do not reuse consumer-session credentials as API keys |
| A model is slow or expensive | Benchmark one short shot before a full run; avoid installing every checkpoint |
| A public Git repository is the destination | Upload generic tooling only; keep personal/private context outside its history |
