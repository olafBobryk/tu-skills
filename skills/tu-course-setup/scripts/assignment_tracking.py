"""Private assignment index and change detection; no remote writes or grade inference."""

import json
import hashlib
from datetime import date, datetime
from zoneinfo import ZoneInfo


def local_time(value, timezone):
    if not value:
        return None
    if len(value) == 10:
        return date.fromisoformat(value).isoformat()
    instant = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if instant.tzinfo is None:
        raise ValueError("Assignment timestamp requires an explicit timezone")
    return instant.astimezone(ZoneInfo(timezone)).isoformat()


def effective_due(assignment):
    sub = assignment.get("submission") or {}
    return sub["cached_due_date"] if "cached_due_date" in sub else assignment.get("due_at")


def reconcile(manifest, previous=None, timezone=None):
    """Return one record per stable source id and explicit changes from the last run.

    Retain unseen records: a missing, unpublished, or inaccessible assignment is
    never evidence to delete a reminder. Null scores remain null.
    """
    course = manifest["course"]
    zone = timezone or course.get("time_zone") or "Europe/Amsterdam"
    platform = manifest.get("platform", "canvas")
    namespace = f"{platform}:{course['url'].rstrip('/')}"
    previous = previous or {}
    records = dict(previous)
    changes = []
    seen = set()
    for assignment in manifest.get("assignments", []):
        key = f"{namespace}:assignment:{assignment['id']}"
        if key in seen:
            raise ValueError(f"Duplicate assignment identity: {key}")
        seen.add(key)
        sub = assignment.get("submission") or {}
        # Canvas applies overrides to due_at by default. cached_due_date is the
        # current student's effective date when explicitly present, including null.
        due = effective_due(assignment)
        record = {
            "key": key, "assignment_id": assignment["id"],
            "name": assignment["name"], "url": assignment.get("html_url"),
            "due_at": due, "due_local": local_time(due, zone), "timezone": zone,
            "unlock_at": assignment.get("unlock_at"), "lock_at": assignment.get("lock_at"),
            "submission": {k: sub[k] for k in (
                "workflow_state", "submitted_at", "graded_at", "attempt", "missing",
                "late", "excused", "score", "grade", "late_policy_status") if k in sub},
            "omit_from_final_grade": assignment.get("omit_from_final_grade"),
            "assignment_group_id": assignment.get("assignment_group_id"),
            "updated_at": assignment.get("updated_at"),
            "description_sha256": hashlib.sha256((assignment.get("description") or "").encode()).hexdigest(),
        }
        old = previous.get(key)
        if old is None:
            changes.append({"key": key, "kind": "new", "after": record})
        elif old != record:
            fields = sorted(k for k in record if old.get(k) != record[k])
            changes.append({"key": key, "kind": "changed", "fields": fields,
                            "before": old, "after": record})
        records[key] = record
    complete = manifest.get("assignments_complete") is True
    for key in previous:
        if key.startswith(namespace + ":assignment:") and key not in seen:
            changes.append({"key": key, "kind": "not_seen" if complete else "collection_incomplete"})
    return records, changes


def write_tracking(manifest, index_path, snapshot, timezone=None):
    previous = json.loads(index_path.read_text(encoding="utf-8")) if index_path.exists() else {}
    records, changes = reconcile(manifest, previous, timezone)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    # Write change report before advancing the index; repeat captures are harmless.
    (snapshot / "assignment-changes.json").write_text(
        json.dumps(changes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary = index_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(index_path)
    coverage_path = index_path.with_name("assignment-coverage.json")
    coverage = {"collected_at": manifest["collected_at"],
                "assignments_complete": manifest.get("assignments_complete"),
                "observed_count": len(manifest.get("assignments", [])),
                "snapshot": snapshot.name, "errors": manifest.get("errors", [])}
    temporary = coverage_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(coverage, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(coverage_path)

