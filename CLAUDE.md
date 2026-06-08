# CLAUDE.md

Guidance for working in this repository.

## What this is

`text-to-respondus` converts Canvas-style quiz `.txt` files into Respondus CSV
(34-column) format for import into LMS systems like ANS. Python, packaged with
Poetry, `src/` layout.

## Layout

- `src/text_to_respondus/parser.py` — parses the quiz text format into dicts.
- `src/text_to_respondus/converter.py` — maps parsed questions to the Respondus
  CSV columns and writes the file (pandas).
- `src/text_to_respondus/cli.py` — the user-facing interface (Click). Entry
  point `text-to-respondus` with subcommands: `convert`, `batch`, `validate`,
  `preview`, `info`. There are intentionally no convenience scripts at the repo
  root; the CLI is the single interface.
- `tests/` — pytest suite (`test_converter.py`, `test_cli.py`).
- `data/example_quiz.txt` — the only tracked sample (see exclusion rule below).

## Commands

```bash
poetry install
poetry run pytest
poetry run text-to-respondus convert data/example_quiz.txt out.csv --topic "Example"
poetry run text-to-respondus batch data/ output/
```

Formatting/typing: `poetry run black src/ tests/` (line length 88),
`poetry run mypy src/`.

## Environment note

Poetry needs a real `python` on PATH. If you use pyenv with the global version
set to `system` (which has only `python3`), Poetry fails with exit code 127.
Fix once in the repo: `pyenv local 3.12.9` (gitignored) then
`poetry env use python`.

## IMPORTANT: course materials are excluded

`data/*.txt` are graded course assignments with the answer keys embedded
(correct option marked `*`, plus a `...` explanation). They are gitignored and
must never be committed. Only `data/example_quiz.txt` is tracked. When adding
real quizzes, keep them in `data/` — the gitignore already excludes them.

## Input format

```
Title: Question category
Points: 1
1. Question text?
... Optional explanation (becomes feedback)
a) Option
*b) Correct option (marked with *)
c) Option
```

A question may carry multiple `*` marks, but the output is single-answer `mc`,
so the parser records the first `*`-marked option as the correct answer.
