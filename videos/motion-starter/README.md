# Launch film motion starter

An actual Remotion/React starter for a restrained startup launch film: large typography, layered spatial cards, real product footage, founder footage and a brand close. Both **LaunchLandscape** (1920×1080) and **LaunchVertical** (1080×1920) run for 18 seconds at 30 fps. The portrait composition rearranges the layout instead of cropping the landscape render.

This is a reusable motion template, not a finished brand film or a claim that it reproduces a reference studio's quality. It contains no generated people, fabricated product metrics or private media. Synthetic geometry and missing-media placeholders are visibly labelled in demo mode.

## Run

Requires Node.js 22 or newer and npm. Packages and the lockfile pin Remotion to **4.0.541**, with matching CLI/media packages and React **19.2.4**.

```sh
npm ci
npm run studio
```

Studio prints its local URL; open it in your browser. The `--no-open` flag avoids launching a browser automatically. Rendering uses Remotion's bundled patched Chrome Headless Shell, downloaded on first render. Network-restricted environments must allow that official browser download; a local browser session is not substituted.

```sh
npm run render
npm run render:vertical
```

Outputs go to `out/`, which is ignored by Git. These commands render the labelled synthetic demo until you supply real media.

## Supply real footage

1. Put an authorized screen recording and founder clip under `public/media/`. Use at least 6.5 seconds of product footage and 5.5 seconds of founder footage; confirm your intended source framing before rendering.
2. Copy `props.example.json` to the ignored `props.local.json`. Set the text, brand colour, founder name/role and local media paths. Media paths are relative to `public/`; remote URLs are rejected by this starter.
3. Keep `demoMode: false` for production. The composition refuses production mode without both product and founder media. This checks that media paths are supplied; factual accuracy and media authenticity still require human review.
4. Render the chosen composition with those props:

```sh
npm run render -- --props=props.local.json
npm run render:vertical -- --props=props.local.json
```

Product footage is muted. Founder source speech is preserved by default. An optional `voiceover` path adds narration across the film and automatically mutes founder source audio to prevent overlapping voices. `founderMuted: true` explicitly silences founder audio even without narration. Supply narration timed to 18 seconds and check loudness and endings in the final edit. No music or voice is bundled.

## Timeline and editing

| Scene | Timeline | Purpose |
|---|---|---|
| Opening thesis | 0–4.5s | Brand, one statement, abstract spatial card stack |
| Product proof | 4–10.5s | Full-frame-preserving real screen recording |
| Founder | 10–15.5s | Real founder clip and lower-third text |
| Close | 15–18s | One call to action |

Overlaps provide brief fades between scenes. Animation comes from Remotion frames, interpolation and deterministic easing; no CSS animation timers are used. Edit authored scene nodes in `src/LaunchFilm.jsx` and registrations in `src/Root.jsx` when changing durations. Recheck safe areas, text lengths, source clip duration and audio at every cut. The spatial geometry is illustrative; replace it with verified spatial/UI content when a film makes actual product claims.

## Verified in this workspace

- `npm install` completed and generated the committed lockfile.
- Studio started and served its preview endpoint at port 3000. No interactive browser inspection was available in this session.
- A 90-frame (3-second) landscape H.264 demo rendered successfully at 1920×1080, 30 fps.
- Landscape and portrait opening stills were visually inspected.
- Product and founder media slots rendered with a neutral local test fixture; a 30-frame narrated founder segment exported with H.264 video and AAC audio.
- Production mode rejects missing product/founder media.

The neutral fixture, dependencies, bundled browser cache and verification exports are untracked and excluded from the project source. A complete 18-second export with your real footage, final narration/music mix and commercial review remains a production task.

## Dependencies and references

[Remotion compositions](https://www.remotion.dev/docs/composition), [media video](https://www.remotion.dev/docs/media/video), [render CLI](https://www.remotion.dev/docs/cli/render), [parameterized renders](https://www.remotion.dev/docs/parameterized-rendering), [Remotion licence](https://www.remotion.dev/license). Check the current licence for your organization and use case; dependencies are not relicensed by this starter.
