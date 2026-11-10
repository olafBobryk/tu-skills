# TU Slide Study Tutor

An agent skill that walks you through a course's lecture slides week by week, spending your time on what the course actually assesses. Built for course folders made by [`tu-course-setup`](../tu-course-setup/README.md), and works with a plain folder of slides too.

**Independent work by Olaf Bobryk. Not an official TU/e or TU Delft product and not affiliated with or endorsed by either university.**

## What it does

1. **Builds each unit around the next deadline.** It finds the next graded assignment, works back to the lectures and exercise sets it covers, and keeps the final exam as a second horizon.
2. **Tiers topics by assessment.** Topics tested by assignments, rubrics or past exams (T1) get questions in the assessed format; exercise-set-only topics (T2) get lighter practice; slide-only topics (T3) get a short note marked "not assessed so far".
3. **Pretests before teaching.** A few quick questions per topic, so it only explains what you missed.
4. **Grades against a real key.** The official solution when one exists; otherwise the model solves the question first and labels its key "model answer, not official".
5. **Keeps what it makes.** Notes, a registry of question types and approaches, a question bank and a miss log go into the course's `study/` folder. Missed concepts come back as warm-up questions in later sessions.
6. **Hands off for the exam.** About three weeks before the exam it suggests an exam-cram skill such as [universal-exam-cram-coach](https://github.com/ZeKaiNie/universal-examprep-skill), pointed at the same folder.

It never works on open graded assignments: before a deadline it writes look-alike practice in the assignment's format instead.

```text
<Course Name> <CODE>/
└── study/
    ├── ledger.md            next deadline, exam date, progress, miss log
    ├── question-types.md    question types, how to spot them, approaches, traps, sources
    ├── notes/<lecture>.md
    └── question-bank/<lecture>.md
```

## Install

```sh
npx skills add olafBobryk/tu-skills --skill tu-slide-study-tutor --agent claude-code
npx skills add olafBobryk/tu-skills --skill tu-slide-study-tutor --agent codex --global
```

Or in Claude Code: `/plugin marketplace add olafBobryk/tu-skills`, then `/plugin install tu-skills --marketplace olafBobryk/tu-skills`.

## Use

- Claude Code: “Study this week's Databases lectures” or `/tu-slide-study-tutor`.
- Codex: “Use $tu-slide-study-tutor to prepare for my next assignment.”

Pace it with `next`, `again`, `deeper`, `quiz me more`, `summarize`, `skip` and `stop`. The [question rules](references/question-rules.md) and [study files](references/study-files.md) references hold the details.

## Validation

New in this release and not yet tested in a full live study session. The design follows research on pretesting, retrieval practice and successive relearning, and on tutors that are given solutions and hold back answers.

## License

[MIT](LICENSE), copyright 2026 Olaf Bobryk.
