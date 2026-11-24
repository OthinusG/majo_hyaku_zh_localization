# MEMORY.md

- Authorized remote is `git@github.com:OthinusG/majo_hyaku_zh_localization.git`, public, and the `main` branch is the push target for verified batches.

- Initial handoff for PS3 `BLJS-10160` combines the 1.00 disc with official updates through 1.40. The two supplied main JSON files were byte-identical. One is the immutable source baseline, the other is the editable `zh` working copy. The baseline SHA-256 is `1f72bf200e53e38b9bc12ff066c3b3a960dd1ccaf75475d78c82cef3d9774dec`.
- The initial CSV is an export snapshot. Its `speaker_or_field` column uses `speaker`, then `field`, then `context`, and `en_ref` maps to JSON `en`.
- `DemoText.dat` stores 259 deduplicated speaker entries before 10,632 dialogue entries. Voice prefixes leave 1,122 dialogue entries with `voice` set to `0`. Batch boundaries use extraction order and stable IDs until a verified chapter mapping is available.
- The handoff description documents image extraction and video scanning. The local material delivered for setup consists of the text corpus and delivery note. Preserve those asset findings as provenance until files can be inspected locally.
