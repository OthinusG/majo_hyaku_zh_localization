# AGENTS.md

## Project

PS3 *The Witch and the Hundred Knight*, Japanese disc `BLJS-10160`, base 1.00 plus official updates through 1.40. See `README.md` for the corpus and `localization_project_plan.md` for scope, batch boundaries, and acceptance criteria.

## Corpus and translation

- Keep `data/source/` immutable. Edit only `entries[].zh` in `data/translation/魔女与百骑兵_中日对照文本.json`. Preserve entry count, order, IDs, metadata, and every other field, including `jp`, `en`, `voice`, `loc`, and `occurrences`.
- Preserve line breaks, tabs, and format tokens in their original order. Keep `placeholder` rows identical to `jp` when filling `zh`. Preserve the `？？？` speaker marker in source metadata. Treat `en` as a reference and translate from `jp` in context.
- Consult `analysis/glossary.md` for terminology. Keep initial CSV and developer/debug material as reference. Put working CSV/TSV files in `tables/` and scratch output in `tmp/`.

## Verification and handoff

- Work on the requested milestone only. Keep batches at or below 1,000 entries. After proofreading and running `python3 scripts/verify_alignment.py`, update the matching checklist item and record its changes in `localization_modification_index.md`.
- Use `python3 scripts/verify_alignment.py --require-complete` for final text acceptance. Review tone, terminology, and layout separately from structural validation. Game import and runtime acceptance have their own milestone.
- With an authorized Git remote, commit each verified batch together with its checklist and modification index, then push to the authorized branch. Follow any user-specified milestone stop point.
- Use Python 3 and the standard library for deterministic tools. Keep extracted game images, binaries, and patch build output under the ignored `assets/` and `build/` directories if they are supplied later.
- Run verifier tests with `python3 -m unittest discover -s scripts` when changing the verifier.
