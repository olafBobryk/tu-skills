# Study files

Everything the tutor writes lives in one `study/` folder in the course folder. It belongs to the student; `course-materials/` is never touched. Files are written during sessions and reused by later sessions and by an exam-cram skill.

```text
<Course Name> <CODE>/
└── study/
    ├── ledger.md              horizons, progress, miss log
    ├── question-types.md      registry of assessed question types and approaches
    ├── notes/<lecture>.md     topic notes, one file per lecture
    └── question-bank/<lecture>.md   asked questions with keys and outcomes
```

Use the lecture's file stem for `<lecture>` (e.g. `lecture2_functional_dependencies`). Link sources with paths relative to the file, and to the snapshot page or assignment when the source is there.

## ledger.md

Navigational only: no explanations or copied content. Read only the header and status table when resuming.

```markdown
# <Course> study ledger

- Course folder: ..
- Next deadline: <assignment> — <date> — covers <lectures>
- Final exam: <date or unknown>
- Exam hand-off: suggest from <date>
- Unit mappings: <assignment> → <lectures> (source: schedule / rubric / asked)

## Status

| Lecture | Exposure | Topic | Tier | State | Last studied |
| --- | --- | --- | --- | --- | --- |

## Miss log

| Date | Type | Concept | What went wrong | Correct sessions | State |
| --- | --- | --- | --- | --- | --- |
```

Exposure: `never seen`, `attended/skimmed`, `studied`; asked at unit start, set to `studied` once all of a lecture's topics are done. States: `todo`, `pretested`, `done`, `skipped`, `locked`. Miss states: `open`, `resolved` (two correct sessions).

## question-types.md

```markdown
# <Course> question types

Built from: <snapshot date> · Updated: <date>

## QT-01 <short type name>

- Tier: T1 · exam-relevant
- Spot it: how the question is recognized
- Approach: 1. … 2. … 3. …
- Traps: common mistakes
- Rubric: criteria and points, when known
- Seen in: [Graded assignment 1 rubric](<path>), [Exercise set 2, ex. 3](<path>), [Exam 2025-02 Q4](<path>)
- Topics: <lecture>/<topic>
```

Number types once and never renumber. Mark a replaced entry `Superseded by QT-NN` instead of deleting it.

## notes/<lecture>.md

Self-contained, exam-focused explanations written after a topic is taught, so they can be reread without the slides.

```markdown
# <Lecture title>

Source: [<slides file>](<path>) · Tier summary: T1 x, T2 y, T3 z

## <Topic> (T1)

- Core idea, definitions in course language, then plain language
- Worked example or small table where the topic needs one
- Approach for its question types: QT-01, QT-04
- Traps
- Slides: <numbers and titles that carry figures>
```

T3 topics get a two-line entry marked "not assessed so far".

## question-bank/<lecture>.md

```markdown
## Q-<lecture>-07 · QT-01 · T1 · <date>

Question: …
Key (official: [Exercise set 2 solutions](<path>) | model answer, not official): …
Outcome: correct | partly | needs work — <one line>
```

Write the key before asking the question. Rephrased miss re-questions get their own entry that refers to the original.
