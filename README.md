# DevOps Attendance Backend

A Flask + Supabase REST API for the attendance management system.

## Project Structure

```
attendance-backend/
├── app.py                    # Flask API entry point (all routes)
├── database.py               # Supabase client + reusable DB helpers
├── student_dashboard/
│   └── dash.py               # Student dashboard logic
├── teacher_dashboard/
│   └── dash.py               # Teacher dashboard logic
├── requirements.txt
├── Procfile                  # For Railway / Render / Heroku deployment
├── .env.example              # Template for secrets
└── .gitignore
```

## Setup (local)

```bash
# 1. Clone and enter the repo
git clone <your-repo-url>
cd attendance-backend

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
cp .env.example .env
# Edit .env with your actual Supabase URL and key

# 5. Run locally
python app.py
```

## Deployment (Railway / Render / Heroku)

1. Push this folder to a GitHub repo.
2. Connect the repo to Railway / Render.
3. Set the following **environment variables** in the platform dashboard:
   - `SUPABASE_URL` — your Supabase project URL
   - `SUPABASE_KEY` — your Supabase service-role key
4. The platform will auto-detect the `Procfile` and run `gunicorn`.

> ⚠️ **Never** commit your `.env` file or paste secrets into source code.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| POST | `/students` | Register a student |
| GET | `/students` | List all students |
| GET | `/students/<enrolment>` | Get one student |
| POST | `/attendance` | Mark attendance |
| GET | `/attendance/student/<enrolment>` | Student's attendance |
| GET | `/attendance/subject/<subject>` | Subject attendance (teacher) |

### POST /students — body
```json
{
  "Enrolment_Number": "07701192024",
  "Name_of_Student": "Vanshika Yadav",
  "Branch": "AIML",
  "College_Email": "abc@igdtuw.com",
  "Semester": "4"
}
```

### POST /attendance — body
```json
{
  "Enrolment_Number": "07701192024",
  "Subject": "DevOps",
  "Date": "2026-04-14",
  "Status": "Present"
}
```

## Supabase Tables Required

**Login_Attendance**
| Column | Type |
|--------|------|
| Enrolment_Number | text (PK) |
| Name_of_Student | text |
| Branch | text |
| College_Email | text |
| Semester | text |

**Attendance**
| Column | Type |
|--------|------|
| id | uuid (auto) |
| Enrolment_Number | text (FK → Login_Attendance) |
| Subject | text |
| Date | date |
| Status | text |
