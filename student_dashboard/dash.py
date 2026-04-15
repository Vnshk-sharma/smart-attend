"""
Student Dashboard helper — called from the frontend (or a separate Flask blueprint).
Provides functions to fetch a student's own attendance summary.
"""

from database import get_student, get_student_attendance


def get_dashboard_data(enrolment_number: str) -> dict:
    """
    Return a structured dashboard payload for the given student.

    Returns:
        {
            "student": { ...profile fields... },
            "attendance": [ ...records... ],
            "summary": {
                "<Subject>": { "total": N, "present": M, "percentage": P }
            }
        }
    """
    student = get_student(enrolment_number)
    if not student:
        raise ValueError(f"No student found with enrolment number: {enrolment_number}")

    records = get_student_attendance(enrolment_number)

    # Build per-subject summary
    summary: dict[str, dict] = {}
    for record in records:
        subject = record.get("Subject", "Unknown")
        if subject not in summary:
            summary[subject] = {"total": 0, "present": 0, "percentage": 0.0}
        summary[subject]["total"] += 1
        if record.get("Status", "").lower() in ("present", "p"):
            summary[subject]["present"] += 1

    for subject, stats in summary.items():
        if stats["total"] > 0:
            stats["percentage"] = round(stats["present"] / stats["total"] * 100, 2)

    return {
        "student": student,
        "attendance": records,
        "summary": summary,
    }
