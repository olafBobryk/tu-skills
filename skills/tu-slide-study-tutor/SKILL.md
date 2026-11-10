---
name: tu-slide-study-tutor
description: >-
  Walk a student through a university course's lecture slides week by week,
  driven by what the course actually assesses. Each unit is built around the
  next graded deadline and the final exam: topics are tiered by whether
  assignments, rubrics and past exams test them, every topic starts with a
  pretest so only the gaps are taught, practice copies the assessed question
  types, and answers are graded against the official solution or the model's
  own prior attempt. Notes, a question-type registry, a question bank and a
  miss log are saved in the course's study/ folder for reuse. Use when a
  student wants to study, go through, or be quizzed on a course's slides or
  weekly content, prepare for the next assignment, or resume a study session.
  For last-weeks exam cramming it hands off to an exam-cram skill.
license: MIT
metadata:
  version: "1.1.0"
---

# TU Slide Study Tutor

Teach a course's weekly content from its slides without spending time on what the course does not assess. The learner sets the pace; the course's assessments set the depth.

Read [question rules](references/question-rules.md) before writing any question and [study files](references/study-files.md) before creating or updating anything in `study/`.

## Inputs

- A course folder, ideally made by `tu-course-setup`: `COURSE.md`, `course-materials/<kind>/`, and the latest `course-materials/<platform>-snapshots/<date>/` (syllabus, pages, `assignments/*.md` with dates and rubrics). Read `COURSE.md` and any `AGENTS.md` first and follow them.
- Without that layout, a plain folder of slides works: ask once where the assignments, exercise sets and past exams are, and tier everything you cannot trace to an assessment as T2 or T3.
- If `COURSE.md`'s sync record says the course context is stale, or material a unit needs is locked or missing, say so and offer a refresh with `tu-course-setup`. Do not refresh without the student's go-ahead.

## Unit start

A unit is the work up to the next graded deadline, with the final exam as the second horizon.

1. **Open the ledger.** Read only the header and status table of `study/ledger.md`. Create `study/` and its files on first use, and add one line for `study/` to the directory map in `COURSE.md` (organizational only; never progress).
2. **Check the AI policy.** On first use, look for an AI or LLM rule in the syllabus, course pages and `COURSE.md`. If the course restricts AI, quote it to the student and ask how they want to proceed before studying; record the rule and any clarification they report (for example from the lecturer) under `COURSE.md`'s agent rules.
3. **Refresh the registry when needed.** If the newest snapshot date is later than the registry's `Built from` date, or the registry does not exist, scan the assessed sources (graded assignments and rubrics, past exams, closed assignments with published solutions, exercise sets, the syllabus's assessment section). Add new question types, source examples and tiers to `study/question-types.md`. Never delete or rewrite existing entries; mark superseded ones.
4. **Pick the unit.** Find the next assessment deadline from the snapshot's assignments: graded homework, or a formative or pass/fail test when that is what the course has. Work back to the lectures and exercise sets it covers using the course schedule, the assignment text, or its rubric; when the mapping is unclear, ask once and record it in the ledger. With no known deadline, follow lecture order.
5. **Ask exposure per lecture.** For each lecture in the unit without an exposure in the ledger, ask once: *never seen*, *attended or skimmed*, or *studied*. Record it in the status table and update it as the learner progresses. Exposure decides the topic loop's opening (see below).
6. **Tier the unit's topics** with the rules in [question rules](references/question-rules.md): T1 assessed, T2 exercise sets only, T3 slides only. Tiers decide how questions are written, not the order of study.
7. **Show a short route:** the deadline, the lectures and topics in teaching order with their tier and exposure, and any locked material. It is a map, not notes.

## Topic loop

For each topic, in teaching order:

1. **Warm-up.** Ask up to 3 re-questions from open misses in the ledger (rephrased, not repeated), oldest first. Skip when there are none.
2. **Open by exposure.**
   - *Attended, skimmed or studied:* **closed-book pretest.** Before teaching, ask 2–3 single-select questions through the harness's question tool (`AskUserQuestion` in Claude Code) plus 1 short written question, drawn from the registry types that fit the topic. Then **teach the gaps**: fully explain only what the pretest missed and confirm what the learner got right in one line.
   - *Never seen:* **teach-through, then open-slides questions.** Give a compact walk-through of the topic with slide numbers, then ask 2–3 open-slides questions (find, apply, explain) that the learner may answer with the slides open. Explain what they got wrong. Never ask closed-book questions on material the learner has not seen.
   - T3 topics get at most one recognition check either way.
   Reuse `study/notes/<lecture>.md` when it already covers the topic instead of explaining from scratch. Course language first, then plain language.
3. **Quiz (closed book).** One round per [question rules](references/question-rules.md), written against the registry type and its rubric. Write each question's key to the question bank before asking. Do not reveal answers in the same message.
4. **Review.** Mark each answer correct, partly correct or needs work; explain the gap; show the key with its provenance label. Do not ask follow-up questions; log misses instead.
5. **Save.** Write or update the topic in the lecture's notes, add the questions and outcomes to the question bank, add misses to the ledger's miss log, and add any new question type or approach to the registry.
6. **Wait.** Stop and wait for the learner's signal before the next topic.

Signals: `next`/`continue`, `again` (re-explain differently), `deeper`, `quiz me more`, `summarize`, `skip` (record it), `stop`. Follow clear intent phrased differently.

## Slides

- Extract text first (`pdftotext`, Python `pypdf`, or the agent's PDF reader, whichever is available). Do not read every page as an image.
- Look at a slide image only when a figure carries the point (diagrams, ER models, worked tables). Show the full slide next to the explanation it supports, labelled with slide number and title.
- Do not infer teaching order or future content from older public material.

## Graded work

- **Open graded assignment:** never answer, hint at, or check the student's answers to its actual questions. Offer look-alike practice in the assignment's format and rubric instead.
- **Closed assignment:** after its deadline it becomes practice. Grade against the official solution once the platform publishes one; until then use the model-answer rule and label it.

## Exam hand-off

Tag topics that appear in past exams as exam-relevant during the term. About three weeks before the exam (date from the syllabus or `COURSE.md`; ask if unknown), suggest switching to an exam-cram skill such as `universal-exam-cram-coach` (`npx skills add ZeKaiNie/universal-examprep-skill`), pointed at the course folder, and name `study/ledger.md` (open misses) and `study/question-types.md` as its starting points. Do not install anything without the student's go-ahead.

## Unit end

Recap the unit in 3–5 bullets, list open misses and likely traps for the deadline, update the ledger status table, and ask what to review before the next unit.

## Rules

- Treat `course-materials/` as immutable.
- Keep `COURSE.md` factual and organizational; progress lives only in `study/`.
- Never present a model answer as official. Never cite a source you did not open.
- Be direct and exam-focused; keep the learner retrieving, explaining and applying rather than reading.
