# Local production commands

The CLI creates reusable planning files and provider prompts. It works without private context and makes no network calls, paid submissions, installations or publishing actions. Python 3 is sufficient.

Run these commands from `videos/`:

```sh
python3 scripts/studio.py init example-reel --track personal
python3 scripts/studio.py status projects/personal/example-reel
python3 scripts/studio.py pack projects/personal/example-reel
```

Use `--track heuro` for the product-marketing track. `init --root /chosen/projects` creates `<root>/<track>/<slug>`. Existing projects are protected: use a new lowercase slug, or edit existing files deliberately.

Each project contains:

- `brief.json`: audience, language, objective, message, CTA, script, references, aspect, duration and budget.
- `storyboard.csv`: timed narration, visual directions and shot kinds.
- `assets.csv`: source/reference asset IDs, private stable storage IDs, rights, checksums and readiness.
- `provider-jobs.json`: provider job IDs, exact conversation handles, state and stable project links.

The initial five-second storyboard is a placeholder. Complete it and match its end time to the brief’s duration. The single-shot timeline must start at zero and have no gaps or overlaps; timing comparisons allow a 1 ms tolerance. Duration values must be finite positive numbers. `status` reports brief gaps, storyboard issues, unresolved assets, context questions and jobs still in flight. `local_plan_complete` means the local plan has its required fields; **it does not establish provider access or video quality**. Provider readiness always requires the connected agent's live check.

`pack` writes `generated/production.md`, `generated/synthesia.md`, `generated/google-scenes.md` and `generated/descript-edit.md`. The prompts combine the supplied brief/storyboard with confirmed preferences and product source context when available. Unknown avatar/voice IDs stay explicitly unverified. Regenerate after editing source files; accepted script edits belong in the brief/storyboard, since the generated files are replaced.

Generated prompts may contain private context. Keep `generated/`, actual project folders and your private context files out of a public Git repository. No account configuration is embedded in the CLI or its tests.

## Bring your context

By default, `pack` and `status` look in `context/`. Shared preferences come from `preferences.json`. The personal track loads only `persona.md`; the product track loads `heuro.md` plus optional `product-context.md`. These documents are included in the production pack and each provider prompt so the chosen track’s context travels with the job. Unrelated track documents are excluded. All files are optional; absent context produces explicit unknowns. `source-register.json` is referenced for provenance when present; its entire cross-track inventory is not copied into prompts. A separate private context directory is supported:

```sh
python3 scripts/studio.py pack projects/personal/example-reel --context /private/context
```

A preference profile is an object with `confirmed` and `unresolved` objects. `confirmed.synthesia_identity_name` supplies the provider identity name to verify. An identity name is not proof that the matching avatar/voice is ready. Never place credentials in a preference profile. This file's confirmed preferences are inserted into generated local prompts.

## Routing

| Storyboard `kind` | Proposed route |
|---|---|
| `speaking` | Synthesia own-avatar segment after identity verification |
| `generated_scene` | Google scene generation after account/model checks |
| `product_capture` | Actual supplied footage |
| `motion_graphic` | Remotion composition |
| `supplied_footage` | Supplied footage |

These are deterministic initial routes, not a universal quality ranking. The agent can choose a benchmarked open-model workflow for a scene and record its execution under `comfyui`. Descript is the proposed assembly/editing step. Exact product UI, parcel evidence and typography should come from actual captures or deterministic graphics.

## Continue provider jobs safely

The connected agent executes provider tools separately, then records identifiers returned by the provider:

```sh
python3 scripts/studio.py record-job projects/personal/example-reel \
  --provider synthesia --job-id example-job-123 --state running \
  --conversation-id example-workspace:example-conversation \
  --url https://example.invalid/project/example-job-123

python3 scripts/studio.py record-job projects/personal/example-reel \
  --provider synthesia --job-id example-job-123 --state done
```

The example identifiers and URL above are placeholders; substitute actual returned values. Updating the same job preserves its handle and link unless explicitly replaced. Another job ID for the same provider is rejected while an earlier job is `queued`, `running` or `needs_answer`. Resolve or continue that job; do not submit a duplicate. Allowed terminal states are `done`, `failed` and `cancelled`.

Only provider IDs and stable HTTPS editor/project links belong in this ledger. Credential-like IDs, query-bearing links and common API/download paths are rejected; extra ledger fields are rejected. This is not a general secret scanner: never paste an API key, session token or signed download link. Use these commands serially; the ledger is a local, single-writer file and does not synchronize concurrent machines.

The `record-job` command does not submit, poll, retry, cancel or reconcile remote jobs. To revise a provider project, the connected agent reuses the recorded conversation handle. Capture model versions and source provenance in the project's asset record or production notes.

## Verification

```sh
python3 -m unittest discover -s tests -v
```

Tests cover protected initialization, invalid slugs, missing private context, track-specific context inclusion and separation, unknown avatar/voice handling, finite durations, timeline gaps/overlaps and float tolerance, job round trips, duplicate-job prevention, signed-link/credential rejection and the distinction between local-plan completeness and provider readiness.
