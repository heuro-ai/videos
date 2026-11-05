# Provider runbooks

These instructions describe connected-agent execution. Read the live tool schemas and relevant installed skill before an actual operation. Provider capabilities and product names can change.

## Synthesia

- Identify the account and workspaces first. Reuse the established workspace; ask which one only when selection is genuinely unresolved.
- Use Syren for new videos by default. Current tools describe a maximum of three minutes per video. Longer requested work needs separate sections and an assembly plan.
- For a personal speaking character, require the matching own avatar and voice. An old draft title or a name supplied in chat does not prove availability. Do not substitute a stock presenter unless requested.
- Record the returned conversation handle unchanged. Poll status with its cursor until done, needs-answer or halted. Answer an actual provider question using known preferences, or ask the user when a necessary choice is unknown.
- Edit through the same conversation rather than creating duplicate videos. Export and publication are separate operations. A preview file is not a finished master. Share links are public to their audience; signed media download URLs should not be stored in Git.

## Descript

- When the Descript plugin and its skills are available, use the create-video skill for import, edit-project for Underlord, and the appropriate transcript, timeline or publish skill for delivery. Find an existing project before creating a replacement.
- Import via supported URLs or the direct upload mechanism. A container file path is not a remote import URL. Save project and composition IDs.
- Underlord edits are asynchronous. Save its conversation ID for later edits, and poll the same job with bounded waits and progress updates. Do not edit the same clip with simultaneous jobs.
- Use social-clip generation for cutdowns, transcript export for SRT/text, and timeline export to continue in another editor. Timeline export does not bundle the underlying media.
- Multiple compositions may require a selection. Verify the completed result and playback rather than trusting an updated timestamp.

## Google video tools

- Verify a connected, signed-in browser or a configured official API route before claiming access. Flow/Gemini subscriptions do not establish API entitlement.
- Consult the current official video documentation for available models; keep model IDs in runtime configuration rather than permanent scripts. Never assume an old preview model still exists.
- Use a per-shot brief with subject, action, camera, lighting, reference assets, aspect ratio, approximate duration and audio intent. Preserve identity references across takes. Edit exact labels and brand typography afterward.
- Keep consumer-browser sessions and API credentials separate. Secrets belong in a secret store/environment, not in prompt files or the repository.

## Local and open-model routes

- Use the catalog to choose a small set for evaluation. Pin source and workflow versions, inspect code and checkpoint licences separately, and verify required hardware.
- ComfyUI workflows, model files and third-party nodes are independently versioned. A workflow JSON is not an installed model. Record the actual checkpoint and node revisions used.
- Use local FFmpeg assembly for available clips; use Remotion for exact graphics and controlled animation when installed. Browser-generated UI footage should come from the actual product, not a model's approximation.

## Job record

For each run retain: project slug, provider, operation, provider job ID, conversation handle, state, last observed time, model/workflow version, reference IDs, selected take, stable result location and reported spend when available. Never store passwords, bearer tokens or signed asset URLs in the ledger.
