"""
Teacher Dashboard helper — provides functions for teacher-side views:
class-wide attendance, per-subject reports, and defaulter lists.
"""

from database import get_all_students, get_attendance_by_subject, supabase


def get_class_summary(subject: str) -> dict:
    """
    Return attendance summary for every student in a given subject.

    Returns:
        {
            "subject": "<subject>",
            "records": [
                {
                    "Enrolment_Number": "...",
                    "Name_of_Student": "...",
                    "total": N,
                    "present": M,
                    "percentage": P
                },
                ...
            ],
            "defaulters": [ ...students below 75% ... ]
        }
    """
    records = get_attendance_by_subject(subject)
    students = get_all_students()

    # Map enrolment → name for display
    student_map = {s["Enrolment_Number"]: s.get("Name_of_Student", "") for s in students}

    # Aggregate per student
    agg: dict[str, dict] = {}
    for r in records:
        en = r.get("Enrolment_Number")
        if en not in agg:
            agg[en] = {
                "Enrolment_Number": en,
                "Name_of_Student": student_map.get(en, "Unknown"),
                "total": 0,
                "present": 0,
                "percentage": 0.0,
            }
        agg[en]["total"] += 1
        if r.get("Status", "").lower() in ("present", "p"):
            agg[en]["present"] += 1

    result = []
    for stats in agg.values():
        if stats["total"] > 0:
            stats["percentage"] = round(stats["present"] / stats["total"] * 100, 2)
        result.append(stats)

    defaulters = [s for s in result if s["percentage"] < 75]

    return {
        "subject": subject,
        "records": result,
        "defaulters": defaulters,
    }


def get_all_subjects() -> list[str]:
    """Return a unique list of subjects that have attendance records."""
    response = supabase.table("Attendance").select("Subject").execute()
    subjects = {r["Subject"] for r in response.data if r.get("Subject")}
    return sorted(subjects)
