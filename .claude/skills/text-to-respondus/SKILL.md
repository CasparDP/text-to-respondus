---
name: text-to-respondus
description: Use when someone wants to convert EXISTING multiple-choice quiz or exam questions into a Respondus CSV for import into an LMS such as ANS, Brightspace, or Canvas, or mentions "Respondus format" or "Canvas-style quiz", or pastes questions / points at a quiz file and asks for an import-ready file. Not for authoring or generating new questions, and not for reviewing or proofreading them.
---

# Converting quizzes to Respondus CSV

## Overview

This repo ships a Python CLI (`text-to-respondus`) that converts a Canvas-style
quiz text file into the 34-column Respondus CSV used by LMS systems like ANS.
**Always drive that CLI; never hand-write the CSV** — the column layout and
escaping are easy to get wrong, and the tool is tested.

Your job with this skill: take whatever quiz the user gives you (often messy,
pasted from Word or email), write it into the input format below, then run the
CLI for them. The user should not need to know any commands.

## When to use

- User has multiple-choice questions and wants a Respondus/ANS import file.
- User points at a `.txt` quiz file, or pastes questions and asks for a CSV.

Not for:
- Writing or generating new questions — this skill only converts questions the
  user already has.
- Reviewing or proofreading questions.
- Question types other than multiple choice — the converter emits single-answer
  `mc` rows only.

## Input format

Save the quiz as a UTF-8 `.txt` file. One block per question:

```
Title: Short category or label
Points: 1
1. The full question text?
... Optional explanation; becomes feedback in the CSV.
a) First option
*b) Correct option (the * marks the answer)
c) Third option
d) Fourth option
```

Rules:
- Each block starts with `Title:` then `Points:`.
- The question line starts with a number and a period (`1.`).
- The `...` explanation line is optional.
- Options run `a)` through `j)` (2–10 allowed). Mark the correct one with a
  leading `*`.
- If several options are marked `*`, the first is used (output is single-answer).
- Any leading `Quiz title:` / `Quiz description:` lines are ignored.

See `data/example_quiz.txt` for a complete example.

## Workflow

1. **Setup once** (if needed): `poetry install`. If Poetry fails with exit code
   127, the environment lacks a usable `python`; see CLAUDE.md (pyenv note).
2. **Write the input** `.txt` from the user's questions in the format above.
3. **Validate**: `poetry run text-to-respondus validate quiz.txt` — confirms it
   parses and reports a question count. Fix format issues before converting.
4. **Convert**:
   - One file: `poetry run text-to-respondus convert quiz.txt out.csv --topic "Week 1"`
   - A folder: `poetry run text-to-respondus batch input_dir/ output_dir/`
5. **Hand back** the CSV path and tell the user to import it into Respondus/ANS.

Use `preview` (`... preview quiz.txt -n 3`) to show the user the first few rows
before committing.

## Common mistakes

- Hand-writing the CSV instead of running the tool. Don't — use the CLI.
- Forgetting the `*` on the correct option (Correct Answer ends up empty).
- Question line missing the leading `1.` — the parser skips it.
- Expecting multi-answer output from several `*` marks; only the first counts.
