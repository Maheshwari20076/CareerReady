# CareerReady
### Student Career Readiness & Skill Gap Analysis System
**BCA Final Year Project Documentation**

---

## 1. Project Introduction

CareerReady is a web-based platform that helps BCA/college students figure out
how ready they are for a career they're interested in. A student picks a
career (e.g. *Python Developer*), tells the system which skills they already
have, and the system compares that against the skills the career actually
requires. It then shows a **readiness percentage**, lists the **missing
skills**, and — most importantly — points the student to **real, trusted
learning resources** for exactly those missing skills. Students can also
practice career-specific interview questions and get a simple keyword-based
score, and track all of this over time on a progress page.

## 2. Problem Statement

Most students choose a career path without a clear, objective way to measure
how prepared they actually are for it. They don't know:
- Which specific skills a career requires.
- How far they are from being "ready."
- Where to find trustworthy resources for the skills they're missing.

Existing platforms (LinkedIn, Internshala, Indeed) focus on jobs and
networking, not on **structured self-assessment and skill-building**.

## 3. Existing System

Currently, students rely on scattered blog posts, YouTube videos, and general
advice from seniors to figure out what to learn for a given career. There is
no single place that:
- Quantifies readiness with a real number.
- Automatically maps missing skills to specific learning resources.
- Lets them practice and score interview questions for that specific role.

## 4. Proposed System

CareerReady solves this with a structured, database-driven workflow:

```
Select Career → View Required Skills → Add Your Skills → Skill Gap Analysis
→ Readiness % → Missing Skills → Matched Learning Resources → Search/Filter
→ Interview Practice → Score → Progress Tracking
```

Everything is calculated dynamically from the MySQL database — nothing is
hardcoded into the HTML.

## 5. Objectives

1. Let students register, log in, and manage a profile.
2. Let students select a career and see its required skills.
3. Let students record the skills they currently have.
4. Dynamically calculate a skill gap and readiness percentage.
5. Recommend real-world learning resources for missing skills.
6. Provide search and filtering across all learning resources.
7. Let students practice interview questions with keyword-based scoring.
8. Give admins full control over careers, skills, resources, and questions.
9. Track a student's progress over time.

## 6. Scope

**In scope:** career readiness assessment, skill gap analysis, admin-curated
learning resource database, basic interview practice, progress tracking.

**Out of scope:** job listings, recruitment, social networking, AI/ML-based
evaluation, resume parsing, payment processing.

## 7. Technologies Used

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Backend | Python 3, Flask (with Flask-Login, Flask-SQLAlchemy) |
| Database | MySQL (via PyMySQL) |
| Dev Tools | VS Code, Git, GitHub, XAMPP |

No AI/ML libraries, paid APIs, or web scraping are used anywhere in the
project.

## 8. System Requirements

**Software:** Python 3.9+, MySQL 8.x (via XAMPP or standalone), a modern
browser, pip.

**Hardware:** Any machine capable of running XAMPP and a Flask development
server (minimum 4GB RAM recommended).

## 9. User Roles

- **Student** — registers, builds a profile, selects a career, manages
  skills, views skill gap & readiness, browses/searches resources, practices
  interviews, tracks progress.
- **Admin** — manages students (read-only view), careers, skills,
  career-skill mappings, learning resources (full CRUD + verify/activate),
  and interview questions.

## 10. System Architecture

CareerReady follows a classic 3-tier architecture:

```
┌─────────────────────┐      ┌─────────────────────┐      ┌──────────────┐
│   Presentation Tier   │ <--> │   Application Tier    │ <--> │   Data Tier   │
│  HTML/CSS/Bootstrap/JS│      │  Flask (Python)        │      │    MySQL      │
└─────────────────────┘      └─────────────────────┘      └──────────────┘
```

Flask is organized using **blueprints** — one per feature area (`auth`,
`student`, `resources`, `interview`, `admin`) — which keep routes grouped and
easy to navigate. SQLAlchemy is used as the ORM layer so the same Python
model classes map directly onto the MySQL tables described in
`database/schema.sql`.

## 11. Modules

1. **Authentication Module** — registration, login, logout, password hashing,
   role-based session handling (`routes/auth.py`).
2. **Student Profile Module** — profile creation/editing (`routes/student.py`).
3. **Career Selection Module** — browsing and selecting a career.
4. **Skill Management Module** — adding/removing a student's current skills.
5. **Skill Gap Module** — comparing required vs. owned skills, calculating
   readiness (`utils.py: calculate_skill_gap`).
6. **Learning Resources Module** — the core feature: skill-based resource
   matching, search, and filtering (`routes/resources.py`).
7. **Interview Practice Module** — career-specific questions and
   keyword-based scoring (`routes/interview.py`).
8. **Progress Tracking Module** — aggregated view of readiness, resources,
   and interview history.
9. **Admin Module** — full CRUD across careers, skills, career-skill
   mappings, resources, and interview questions (`routes/admin.py`).

## 12. Database Design

Nine tables, all connected by foreign keys:

`users` · `student_profiles` · `skills` · `student_skills` · `career_roles`
· `career_skills` · `learning_resources` · `interview_questions` ·
`interview_attempts`

The full column-by-column definitions and constraints are in
`database/schema.sql`. Key relationships:

- One `user` has one `student_profile` (1:1).
- One `career_role` has many `career_skills`, which link to `skills` (M:N
  via a join table).
- One `skill` has many `learning_resources` (1:N).
- One `student` has many `student_skills` (M:N with `skills`).
- One `career_role` has many `interview_questions`; a `student` accumulates
  many `interview_attempts`.

## 13. ER Diagram (description)

```
users (1) ──── (1) student_profiles ──── (N:1) career_roles
  │                                              │
  │ (1:N)                                        │ (1:N)
  ▼                                              ▼
student_skills (N:1)──► skills ◄──(N:1) career_skills
                          │
                          │ (1:N)
                          ▼
                 learning_resources

career_roles (1:N) interview_questions (1:N) interview_attempts (N:1) users
```

## 14. User Flow

```
Landing → Register → Login → Dashboard → Profile → Select Career
→ View Required Skills → Add Skills → Skill Gap → Readiness %
→ Missing Skills → Learning Resources (search/filter) → Open Resource
→ Interview Practice → Score → Progress
```

## 15. Skill Gap Algorithm

For a given student and their selected career:

```
required_skills = skills mapped to the selected career (career_skills table)
owned_skills    = skills the student added (student_skills table)

matched_skills  = required_skills ∩ owned_skills
missing_skills  = required_skills − owned_skills

readiness % = (count(matched_skills) / count(required_skills)) × 100
```

Readiness levels:

| Range | Level |
|---|---|
| 0–30% | Beginner |
| 31–60% | Developing |
| 61–80% | Job Ready |
| 81–100% | Highly Ready |

This is implemented once, in `utils.py`, and reused everywhere (dashboard,
skill-gap page, resources page, progress page, admin student detail) so the
number is always consistent and always computed from the database — never
hardcoded.

## 16. Resource Matching Logic

1. Get the student's `missing_skills` from the skill gap algorithm above.
2. For each missing skill, query `learning_resources` where
   `skill_id = missing_skill.id AND is_active = TRUE`.
3. Group results by skill and display under **"Recommended for You"**.
4. Separately, the **"Explore All Resources"** section supports free-text
   search (title, provider, description, skill name) combined with skill /
   type / level filters and simple sorting — all resolved as one SQLAlchemy
   query, so search and filters can be combined.

When an admin deactivates a resource, it immediately disappears from student
pages — no restart or redeploy needed, because the student query always
filters on `is_active = TRUE`.

## 17. Interview Evaluation Logic

This is **not** an AI evaluation. Each question has an admin-defined,
comma-separated list of expected keywords. The score is:

```
score % = (number of expected keywords found in the student's answer
           / total expected keywords) × 100
```

Matching is case-insensitive substring matching (see
`utils.py: score_interview_answer`). Every attempt (question, answer, score,
timestamp) is stored in `interview_attempts` so it can be shown in the
progress page.

## 18. Security

- Passwords are hashed with Werkzeug's `generate_password_hash` /
  `check_password_hash` — never stored in plain text.
- Sessions are handled by Flask-Login.
- Role-based route protection via `@admin_required` / `@student_required`
  decorators (`utils.py`) — a student hitting an `/admin/...` route gets a
  clean 403 page, and vice versa.
- All database access goes through SQLAlchemy's parameterized queries, which
  prevents SQL injection.
- External resource links always open with
  `target="_blank" rel="noopener noreferrer"`.
- Server-side validation on all forms (required fields, URL format, duplicate
  checks) in addition to basic HTML5 client-side validation.

## 19. Testing

Manual and scripted testing was performed for:

- **Auth:** registration, duplicate-email rejection, login/logout, invalid
  credentials.
- **Career & Skills:** career selection, adding/removing skills, duplicate
  skill prevention.
- **Skill Gap:** matched/missing calculation and readiness percentage against
  a known dataset (Python Developer example: 4/7 skills → 57.1% →
  "Developing").
- **Resources:** recommended-for-you matching, search, skill/type/level
  filters (individually and combined), external link correctness, admin
  add/edit/delete, and activation/verification toggles (confirmed an
  inactive resource is immediately hidden from students).
- **Interview:** question loading per career, keyword-based scoring, attempt
  storage.
- **Admin:** protected-route enforcement (403 for non-admins) and CRUD
  operations across all admin-managed entities.

All of the above were verified end-to-end using Flask's test client against
a seeded database before this project was delivered.

## 20. Future Enhancements

- Email verification and password-reset flow.
- Resume upload and basic keyword extraction (still without AI).
- Skill endorsements or peer review.
- Exportable readiness report (PDF).
- Admin analytics dashboard (most-missing skills across all students, most-
  clicked resources).

## 21. Conclusion

CareerReady gives students a simple, honest, database-driven way to answer
the question *"How ready am I, what's missing, and where do I learn it?"* —
without relying on AI, scraping, or guesswork. The architecture (Flask +
MySQL, clearly separated modules) keeps the project easy to explain in a
viva while still being a fully working, end-to-end application rather than a
static mockup.

---

## Viva Quick-Reference

**What is CareerReady?**
A platform that helps students measure their career readiness, identify
missing skills, find real-world learning resources, and practice interviews.

**How is readiness calculated?**
Matched required skills ÷ total required skills × 100 — computed live from
the database every time the page loads.

**How are resources recommended?**
The system finds the student's missing skills, then queries
`learning_resources` for active resources tied to those skill IDs.

**Is resource recommendation AI?** No — it's plain database-driven matching.

**How are interview answers evaluated?**
Keyword matching: number of expected keywords found in the answer ÷ total
expected keywords.

**Is interview evaluation AI?** No.

**Why Flask?** Lightweight, simple to read, and well suited to a
beginner-to-intermediate Python web project.

**Why MySQL?** A structured relational database is a natural fit for the
clearly related entities here (students, careers, skills, resources,
questions).

**Why admin-curated resources instead of scraping/AI?** It keeps links
reliable and verifiable, avoids legal/technical complexity, and is easy to
explain and maintain in a student project.

---

## Setup Instructions (XAMPP / MySQL)

1. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Start MySQL from XAMPP, then create the database — either:
   - Import `database/schema.sql` via phpMyAdmin, **or**
   - Just let step 4 create the tables automatically.
3. Copy `.env.example` to `.env` and fill in your MySQL credentials
   (defaults already match a fresh XAMPP install).
4. Seed the database with sample careers, skills, resources, and demo
   accounts:
   ```
   python seed.py
   ```
5. Run the app:
   ```
   python app.py
   ```
6. Visit `http://localhost:5000`.

**Demo accounts:**
- Student — `student@demo.com` / `student123`
- Admin — `admin@demo.com` / `admin123`
