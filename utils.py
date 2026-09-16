"""
Shared helper functions: skill-gap calculation, readiness level, and
keyword-based interview scoring. Kept in one place so the logic is
calculated dynamically everywhere it's used, never hardcoded.
"""

from functools import wraps
from flask import abort
from flask_login import current_user

from models import CareerSkill, StudentSkill, Skill


def admin_required(f):
    """Route decorator: only allow logged-in users with role='admin'."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated


def student_required(f):
    """Route decorator: only allow logged-in users with role='student'."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated


def get_required_skills(career_id):
    """Return list of Skill objects required for a career."""
    if not career_id:
        return []
    career_skills = CareerSkill.query.filter_by(career_id=career_id).all()
    return [cs.skill for cs in career_skills]


def get_student_skills(student_id):
    """Return list of Skill objects the student currently has."""
    student_skills = StudentSkill.query.filter_by(student_id=student_id).all()
    return [ss.skill for ss in student_skills]


def calculate_skill_gap(student_id, career_id):
    """
    Compare required career skills with the student's current skills.
    Returns a dict with matched skills, missing skills, and readiness info.
    """
    required = get_required_skills(career_id)
    owned = get_student_skills(student_id)
    owned_ids = {s.id for s in owned}

    matched = [s for s in required if s.id in owned_ids]
    missing = [s for s in required if s.id not in owned_ids]

    total_required = len(required)
    total_matched = len(matched)

    readiness_percent = round((total_matched / total_required) * 100, 1) if total_required else 0
    readiness_level = get_readiness_level(readiness_percent)

    return {
        "required": required,
        "matched": matched,
        "missing": missing,
        "total_required": total_required,
        "total_matched": total_matched,
        "readiness_percent": readiness_percent,
        "readiness_level": readiness_level,
    }


def get_readiness_level(percent):
    if percent <= 30:
        return "Beginner"
    elif percent <= 60:
        return "Developing"
    elif percent <= 80:
        return "Job Ready"
    else:
        return "Highly Ready"


def score_interview_answer(answer, expected_keywords_csv):
    """
    Very simple keyword-based scoring (NOT AI-based):
    score = (number of expected keywords found in the answer / total expected keywords) * 100
    Matching is case-insensitive and ignores extra whitespace.
    """
    if not expected_keywords_csv:
        return 0.0

    expected_keywords = [k.strip().lower() for k in expected_keywords_csv.split(",") if k.strip()]
    if not expected_keywords:
        return 0.0

    answer_lower = (answer or "").lower()
    matched = sum(1 for kw in expected_keywords if kw in answer_lower)

    return round((matched / len(expected_keywords)) * 100, 1)
