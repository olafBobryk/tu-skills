# Assignment audit and deadline reconciliation

Keep this work in the student's private course library, outside the public skill repository. Never commit real captures, grades, student identifiers, course plans, Calendar/Tasks ids, or submission records. Use invented fixtures for testing.

## Verify coursework

1. Enumerate every current course and follow pagination. In each course inspect assignments and quizzes, syllabus, announcements, and linked assessment pages. A calendar feed alone is not a complete assignment list.
2. Record the signed-in student's effective due date (including overrides), availability cutoff, submission state, actual submitted time, and posted score separately. Keep exact timestamps with timezone; use Europe/Amsterdam for TU/e. Date-only sources stay date-only. An unlock date is not a deadline, and a lock date is not permission to submit late.
3. Distinguish submitted but ungraded, not submitted, explicitly missing, late, excused, and unavailable status. A null/hidden grade is unknown, never zero. Group work and external tools may require a separate status check. Do not open/start/reopen a quiz attempt merely to inspect it.
4. Read the current published assessment rules: weights, dropped scores, mandatory participation, component minima, late policy, resits and replacement rules. Canvas's displayed total may omit ungraded work. Explain any grade projection as a conditional calculation, with assumptions; do not change grades or submit coursework.
5. Lead the report with the earliest still-actionable deadline. Separate verified make-up opportunities from questions requiring staff confirmation. Do not message staff without the student's authorization.

## Track changes during import

The organizer writes `course-materials/<platform>-snapshots/assignment-index.json`, keyed by platform + course URL + assignment id, and a dated `assignment-changes.json`. Always read `assignment-coverage.json` beside the index: it records the last capture time, completeness, observed count, snapshot and errors, including when older records were retained. Refreshes update the same key even if a name or due date changes. Failed collection is distinct from a successful empty list. Missing records are retained and flagged for review, never automatically removed. The index preserves unknown scores and exact local timestamps. These files are private data, not public skill assets.

Canvas collection requests the current user's submission summary and effective override dates, plus assignment-group weights and drop rules. If the API is inaccessible or the browser forbids page requests, inspect the UI and mark collection incomplete. Do not claim full coverage from an empty result. Brightspace assignment-status collection remains experimental; unknown status must stay unknown.

## Reconcile Calendar and Google Tasks when authorized

Use connected tools. Store the following ledger privately at `<course>/notes/deadline-sync.json` (create `notes/` if necessary), separate from immutable course material:

- Source key and canonical assignment URL; source due timestamp and time zone.
- Calendar id/event id and Tasks list id/task id; last confirmed fields and verification time.
- Any pending/uncertain write, so a later run searches for it before creating again.

For each verified assignment:

1. Read the full existing task lists (including undated and completed tasks) and page through Calendar candidates in the course's relevant date range. For deadline changes, search both the previous and new date ranges; also search by canonical URL or course/assignment name. Existing user reminders without importer markers count as candidates.
2. Match the stable source key first, then the canonical assignment URL. For older reminders, require a unique course + assignment match and read it before adopting it into the ledger. Ambiguous matches require review; never create a second reminder to resolve ambiguity. A changed title/date does not create a new identity.
3. Put `TU-ASSIGNMENT-KEY: <source key>` and the canonical source URL in the event description/task notes. Preserve user notes, reminders, priority, and chosen task dates. Apply changes only to source-owned fields. Read each object before updating it.
4. Calendar records the actual deadline. For an exact deadline use a timed event beginning at that instant (for example, a 5-minute transparent marker); retain exact seconds and local timezone. For a date-only deadline use an all-day event and say that the time is unspecified. Never fabricate a time.
5. Tasks represent outstanding work. Google Tasks dates are scheduled days, not exact deadlines; store the actual deadline, timezone, published late policy and source in notes. Do not reopen a completed task or move its scheduled day solely because a deadline changed; flag it for review. Submitted-but-ungraded work needs no submit task unless another verified action remains.
6. Create only after the duplicate check is complete. Read back every create/update, verify its source key, date, destination and status, then save the returned ids to the ledger. Persist an intent before a create. On a timeout or uncertain result, search and reconcile instead of blindly retrying. Missing/deleted ledger targets must be investigated before recreation.
7. If a date disappears, a course becomes inaccessible, or source rules conflict, flag it; do not erase reminders or silently replace a known deadline. Report coverage gaps and unresolved changes.

The organizer detects changes; the agent applies them through authorized connected tools. It does not itself call Calendar or Tasks, create a background schedule, or infer permission for future unattended writes.
