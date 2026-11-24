"""Synthetic regression cases only; run with python3 -m unittest discover -s scripts."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from assignment_tracking import local_time, reconcile


def fixture():
    return {
        "schema": 2, "assignments_complete": True,
        "collected_at": "2030-01-01T12:00:00Z", "code": "TEST100",
        "course": {"id": 123, "name": "Invented Course", "url": "https://canvas.example/courses/123"},
        "files": [], "modules": [], "pages": [], "announcements": [],
        "assignments": [{"id": 1, "name": "Invented assignment", "due_at": "2030-01-02T16:00:00Z",
                         "html_url": "https://canvas.example/courses/123/assignments/1",
                         "submission": {"workflow_state": "submitted", "score": None}}],
    }


class TrackingTests(unittest.TestCase):
    def test_setup_repeat_and_changed_deadline_keep_identity(self):
        m = fixture()
        index, changes = reconcile(m)
        self.assertEqual(changes[0]["kind"], "new")
        self.assertIsNone(next(iter(index.values()))["submission"]["score"])
        self.assertEqual(reconcile(m, index), (index, []))
        m["assignments"][0].update(name="Renamed", due_at="2030-01-03T16:00:00Z")
        refreshed, changes = reconcile(m, index)
        self.assertEqual(set(index), set(refreshed))
        self.assertIn("due_at", changes[0]["fields"])
        self.assertEqual(len(refreshed), 1)

    def test_date_only_remains_date_only(self):
        self.assertEqual(local_time("2030-01-02", "Europe/Amsterdam"), "2030-01-02")

    def test_effective_null_and_dst(self):
        m = fixture()
        m["assignments"][0]["submission"]["cached_due_date"] = None
        self.assertIsNone(next(iter(reconcile(m)[0].values()))["due_at"])
        m["assignments"][0]["submission"]["cached_due_date"] = "2030-07-02T15:00:30Z"
        record = next(iter(reconcile(m)[0].values()))
        self.assertEqual(record["due_local"], "2030-07-02T17:00:30+02:00")

    def test_failed_and_empty_collection_retain_records(self):
        m = fixture()
        index, _ = reconcile(m)
        m["assignments"] = []
        m["assignments_complete"] = False
        retained, changes = reconcile(m, index)
        self.assertEqual(retained, index)
        self.assertEqual(changes[0]["kind"], "collection_incomplete")
        m["assignments_complete"] = True
        self.assertEqual(reconcile(m, index)[1][0]["kind"], "not_seen")

    def test_courses_do_not_collide_and_duplicates_fail(self):
        m = fixture()
        index, _ = reconcile(m)
        m["course"]["url"] = "https://another.example/courses/123"
        self.assertEqual(len(reconcile(m, index)[0]), 2)
        m["assignments"].append(copy.deepcopy(m["assignments"][0]))
        with self.assertRaises(ValueError):
            reconcile(m)

    def test_organizer_setup_and_refresh(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            downloads, course = root / "downloads", root / "course"
            downloads.mkdir()
            mapping = root / "mapping.json"
            mapping.write_text(json.dumps({"code": "TEST100", "course_name": "Invented Course", "modules": {}}))
            script = Path(__file__).with_name("organize_course.py")
            command = [sys.executable, str(script), "--downloads", str(downloads),
                       "--course-dir", str(course), "--mapping", str(mapping)]
            manifest = downloads / "TEST100__manifest.json"
            m = fixture()
            for run in range(3):
                if run == 2:
                    m["assignments"][0]["due_at"] = "2030-01-04T16:00:00Z"
                m["assignments"][0]["submission"]["cached_due_date"] = m["assignments"][0]["due_at"]
                manifest.write_text(json.dumps(m))
                subprocess.run(command, check=True, capture_output=True)
                self.assertFalse((course / "COURSE.md").exists() and run == 0)
                subprocess.run(command + ["--move"], check=True, capture_output=True)
            snapshots = course / "course-materials/canvas-snapshots"
            index = json.loads((snapshots / "assignment-index.json").read_text())
            self.assertEqual(len(index), 1)
            self.assertEqual(json.loads((snapshots / "2030-01-01-2/assignment-changes.json").read_text()), [])
            changes = json.loads((snapshots / "2030-01-01-3/assignment-changes.json").read_text())
            self.assertEqual(changes[0]["kind"], "changed")
            text = (snapshots / "2030-01-01/assignments/invented-assignment.md").read_text()
            self.assertIn("2030-01-02T17:00:00+01:00", text)
            m["assignments"][0]["submission"]["cached_due_date"] = "2030-02-01T15:30:42Z"
            manifest.write_text(json.dumps(m))
            subprocess.run(command + ["--move"], check=True, capture_output=True)
            text = (snapshots / "2030-01-01-4/assignments/invented-assignment.md").read_text()
            self.assertIn("2030-02-01T16:30:42+01:00", text)
            m.update(assignments=[], assignments_complete=False, errors=["assignments: 403 synthetic"])
            manifest.write_text(json.dumps(m))
            subprocess.run(command + ["--move"], check=True, capture_output=True)
            self.assertIn("Assignment coverage INCOMPLETE", (course / "COURSE.md").read_text())
            coverage = json.loads((snapshots / "assignment-coverage.json").read_text())
            self.assertIs(coverage["assignments_complete"], False)
            self.assertEqual(len(json.loads((snapshots / "assignment-index.json").read_text())), 1)


if __name__ == "__main__":
    unittest.main()
