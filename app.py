from flask import Flask, request, jsonify
from flask_cors import CORS
from database import (
    insert_student,
    get_student,
    get_all_students,
    mark_attendance,
    get_student_attendance,
    get_attendance_by_subject,
)

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from your frontend


# ── Health check ─────────────────────────────────────────────────────────────

@app.get("/")
def health():
    return jsonify({"status": "ok", "message": "Attendance backend is running."})


# ── Student routes ────────────────────────────────────────────────────────────

@app.post("/students")
def add_student():
    """Register a new student."""
    body = request.get_json()
    required = ["Enrolment_Number", "Name_of_Student", "Branch", "College_Email", "Semester"]
    missing = [f for f in required if f not in body]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        result = insert_student(body)
        return jsonify({"success": True, "data": result}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/students")
def list_students():
    """Get all students (teacher use)."""
    try:
        students = get_all_students()
        return jsonify(students)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/students/<enrolment_number>")
def get_one_student(enrolment_number: str):
    """Get a single student by enrolment number."""
    try:
        student = get_student(enrolment_number)
        if not student:
            return jsonify({"error": "Student not found"}), 404
        return jsonify(student)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Attendance routes ─────────────────────────────────────────────────────────

@app.post("/attendance")
def add_attendance():
    """Mark attendance for a student."""
    body = request.get_json()
    required = ["Enrolment_Number", "Subject", "Date", "Status"]
    missing = [f for f in required if f not in body]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        result = mark_attendance(body)
        return jsonify({"success": True, "data": result}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/attendance/student/<enrolment_number>")
def student_attendance(enrolment_number: str):
    """Get attendance records for a specific student."""
    try:
        records = get_student_attendance(enrolment_number)
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/attendance/subject/<subject>")
def subject_attendance(subject: str):
    """Get all attendance records for a subject (teacher view)."""
    try:
        records = get_attendance_by_subject(subject)
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # For local development only — use gunicorn in production
    app.run(debug=False, host="0.0.0.0", port=5000)
