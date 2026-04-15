import os
from supabase import create_client, Client

# 🔑 Load credentials from environment variables (never hardcode these!)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError(
        "Missing required environment variables: SUPABASE_URL and SUPABASE_KEY must be set."
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_supabase() -> Client:
    """Return the shared Supabase client."""
    return supabase


# ── Student helpers ──────────────────────────────────────────────────────────

def insert_student(data: dict) -> dict:
    """
    Insert a student login record into Login_Attendance.
    Expected keys: Enrolment_Number, Name_of_Student, Branch, College_Email, Semester
    """
    response = supabase.table("Login_Attendance").insert(data).execute()
    return response.data


def get_student(enrolment_number: str) -> dict | None:
    """Fetch a student record by enrolment number."""
    response = (
        supabase.table("Login_Attendance")
        .select("*")
        .eq("Enrolment_Number", enrolment_number)
        .single()
        .execute()
    )
    return response.data


def get_all_students() -> list:
    """Fetch all student records."""
    response = supabase.table("Login_Attendance").select("*").execute()
    return response.data


# ── Attendance helpers ────────────────────────────────────────────────────────

def mark_attendance(data: dict) -> dict:
    """
    Insert an attendance record.
    Expected keys depend on your Supabase table schema, e.g.:
      Enrolment_Number, Subject, Date, Status
    """
    response = supabase.table("Attendance").insert(data).execute()
    return response.data


def get_student_attendance(enrolment_number: str) -> list:
    """Fetch all attendance records for a given student."""
    response = (
        supabase.table("Attendance")
        .select("*")
        .eq("Enrolment_Number", enrolment_number)
        .execute()
    )
    return response.data


def get_attendance_by_subject(subject: str) -> list:
    """Fetch all attendance records for a given subject."""
    response = (
        supabase.table("Attendance")
        .select("*")
        .eq("Subject", subject)
        .execute()
    )
    return response.data
