from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models import db, StudentProfile, CareerRole, Skill, StudentSkill, LearningResource, InterviewAttempt
from utils import calculate_skill_gap, student_required

student_bp = Blueprint("student", __name__)


def _ensure_profile():
    """Every student should have a profile row; create one on first access."""
    if not current_user.profile:
        profile = StudentProfile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
    return current_user.profile


@student_bp.route("/dashboard")
@login_required
@student_required
def dashboard():
    profile = _ensure_profile()
    career = profile.career

    gap = calculate_skill_gap(current_user.id, career.id if career else None)

    resource_count = 0
    if gap["missing"]:
        missing_ids = [s.id for s in gap["missing"]]
        resource_count = LearningResource.query.filter(
            LearningResource.skill_id.in_(missing_ids),
            LearningResource.is_active.is_(True),
        ).count()

    latest_attempt = (
        InterviewAttempt.query.filter_by(student_id=current_user.id)
        .order_by(InterviewAttempt.created_at.desc())
        .first()
    )

    return render_template(
        "student/dashboard.html",
        career=career,
        gap=gap,
        resource_count=resource_count,
        latest_score=latest_attempt.score if latest_attempt else None,
    )


@student_bp.route("/profile", methods=["GET", "POST"])
@login_required
@student_required
def profile():
    profile = _ensure_profile()

    if request.method == "POST":
        current_user.name = request.form.get("name", current_user.name).strip()
        profile.phone = request.form.get("phone", "").strip()
        profile.college = request.form.get("college", "").strip()
        profile.degree = request.form.get("degree", "").strip()
        grad_year = request.form.get("graduation_year", "").strip()
        profile.graduation_year = int(grad_year) if grad_year.isdigit() else None
        profile.location = request.form.get("location", "").strip()
        profile.bio = request.form.get("bio", "").strip()

        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("student.profile"))

    return render_template("student/profile.html", profile=profile)


@student_bp.route("/careers")
@login_required
@student_required
def careers():
    profile = _ensure_profile()
    all_careers = CareerRole.query.order_by(CareerRole.name).all()
    return render_template("student/careers.html", careers=all_careers, current_career_id=profile.career_id)


@student_bp.route("/careers/select/<int:career_id>", methods=["POST"])
@login_required
@student_required
def select_career(career_id):
    profile = _ensure_profile()
    career = CareerRole.query.get_or_404(career_id)
    profile.career_id = career.id
    db.session.commit()
    flash(f"You selected {career.name} as your target career.", "success")
    return redirect(url_for("student.skill_gap"))


@student_bp.route("/skills", methods=["GET", "POST"])
@login_required
@student_required
def skills():
    if request.method == "POST":
        skill_id = request.form.get("skill_id")
        skill = Skill.query.get(skill_id) if skill_id else None
        if not skill:
            flash("Please select a valid skill.", "danger")
        elif StudentSkill.query.filter_by(student_id=current_user.id, skill_id=skill.id).first():
            flash("You already added this skill.", "warning")
        else:
            db.session.add(StudentSkill(student_id=current_user.id, skill_id=skill.id))
            db.session.commit()
            flash(f"Added skill: {skill.name}", "success")
        return redirect(url_for("student.skills"))

    my_skills = StudentSkill.query.filter_by(student_id=current_user.id).all()
    my_skill_ids = {ss.skill_id for ss in my_skills}
    available_skills = Skill.query.filter(~Skill.id.in_(my_skill_ids)).order_by(Skill.name).all() if my_skill_ids else Skill.query.order_by(Skill.name).all()

    return render_template("student/skills.html", my_skills=my_skills, available_skills=available_skills)


@student_bp.route("/skills/remove/<int:student_skill_id>", methods=["POST"])
@login_required
@student_required
def remove_skill(student_skill_id):
    ss = StudentSkill.query.filter_by(id=student_skill_id, student_id=current_user.id).first_or_404()
    db.session.delete(ss)
    db.session.commit()
    flash("Skill removed.", "info")
    return redirect(url_for("student.skills"))


@student_bp.route("/skill-gap")
@login_required
@student_required
def skill_gap():
    profile = _ensure_profile()
    if not profile.career:
        flash("Select a career to start your readiness assessment.", "warning")
        return redirect(url_for("student.careers"))

    gap = calculate_skill_gap(current_user.id, profile.career_id)
    return render_template("student/skill_gap.html", career=profile.career, gap=gap)


@student_bp.route("/progress")
@login_required
@student_required
def progress():
    profile = _ensure_profile()
    career = profile.career
    gap = calculate_skill_gap(current_user.id, career.id if career else None)

    attempts = (
        InterviewAttempt.query.filter_by(student_id=current_user.id)
        .order_by(InterviewAttempt.created_at.desc())
        .all()
    )
    avg_score = round(sum(a.score for a in attempts) / len(attempts), 1) if attempts else 0

    resources_explored = 0  # simple placeholder metric; count of active resources for missing skills
    if gap["missing"]:
        missing_ids = [s.id for s in gap["missing"]]
        resources_explored = LearningResource.query.filter(
            LearningResource.skill_id.in_(missing_ids),
            LearningResource.is_active.is_(True),
        ).count()

    return render_template(
        "student/progress.html",
        career=career,
        gap=gap,
        attempts=attempts,
        avg_score=avg_score,
        resources_explored=resources_explored,
    )
