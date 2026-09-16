from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from models import (
    db, User, CareerRole, Skill, CareerSkill, LearningResource,
    InterviewQuestion, StudentProfile,
)
from utils import calculate_skill_gap, admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ---------------------------------------------------------------- DASHBOARD
@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    stats = {
        "total_students": User.query.filter_by(role="student").count(),
        "total_careers": CareerRole.query.count(),
        "total_skills": Skill.query.count(),
        "total_resources": LearningResource.query.count(),
        "verified_resources": LearningResource.query.filter_by(is_verified=True).count(),
        "active_resources": LearningResource.query.filter_by(is_active=True).count(),
        "total_questions": InterviewQuestion.query.count(),
    }
    recent_students = User.query.filter_by(role="student").order_by(User.created_at.desc()).limit(5).all()
    return render_template("admin/dashboard.html", stats=stats, recent_students=recent_students)


# ---------------------------------------------------------------- STUDENTS
@admin_bp.route("/students")
@login_required
@admin_required
def students():
    search = request.args.get("q", "").strip()
    q = User.query.filter_by(role="student")
    if search:
        like = f"%{search}%"
        q = q.filter(db.or_(User.name.ilike(like), User.email.ilike(like)))
    all_students = q.order_by(User.name).all()

    student_info = []
    for s in all_students:
        career = s.profile.career if s.profile else None
        gap = calculate_skill_gap(s.id, career.id if career else None)
        student_info.append({"user": s, "career": career, "readiness": gap["readiness_percent"]})

    return render_template("admin/students.html", student_info=student_info, search=search)


@admin_bp.route("/students/<int:user_id>")
@login_required
@admin_required
def student_detail(user_id):
    student = User.query.filter_by(id=user_id, role="student").first_or_404()
    career = student.profile.career if student.profile else None
    gap = calculate_skill_gap(student.id, career.id if career else None)
    return render_template("admin/student_detail.html", student=student, career=career, gap=gap)


# ---------------------------------------------------------------- CAREERS
@admin_bp.route("/careers", methods=["GET", "POST"])
@login_required
@admin_required
def careers():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        if not name:
            flash("Career name is required.", "danger")
        elif CareerRole.query.filter_by(name=name).first():
            flash("A career with this name already exists.", "warning")
        else:
            db.session.add(CareerRole(name=name, description=description))
            db.session.commit()
            flash("Career added.", "success")
        return redirect(url_for("admin.careers"))

    all_careers = CareerRole.query.order_by(CareerRole.name).all()
    return render_template("admin/careers.html", careers=all_careers)


@admin_bp.route("/careers/edit/<int:career_id>", methods=["POST"])
@login_required
@admin_required
def edit_career(career_id):
    career = CareerRole.query.get_or_404(career_id)
    career.name = request.form.get("name", career.name).strip()
    career.description = request.form.get("description", "").strip()
    db.session.commit()
    flash("Career updated.", "success")
    return redirect(url_for("admin.careers"))


@admin_bp.route("/careers/delete/<int:career_id>", methods=["POST"])
@login_required
@admin_required
def delete_career(career_id):
    career = CareerRole.query.get_or_404(career_id)
    db.session.delete(career)
    db.session.commit()
    flash("Career deleted.", "info")
    return redirect(url_for("admin.careers"))


# ---------------------------------------------------------------- SKILLS
@admin_bp.route("/skills", methods=["GET", "POST"])
@login_required
@admin_required
def skills():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        if not name:
            flash("Skill name is required.", "danger")
        elif Skill.query.filter_by(name=name).first():
            flash("This skill already exists.", "warning")
        else:
            db.session.add(Skill(name=name, description=description))
            db.session.commit()
            flash("Skill added.", "success")
        return redirect(url_for("admin.skills"))

    search = request.args.get("q", "").strip()
    q = Skill.query
    if search:
        q = q.filter(Skill.name.ilike(f"%{search}%"))
    all_skills = q.order_by(Skill.name).all()
    return render_template("admin/skills.html", skills=all_skills, search=search)


@admin_bp.route("/skills/edit/<int:skill_id>", methods=["POST"])
@login_required
@admin_required
def edit_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    skill.name = request.form.get("name", skill.name).strip()
    skill.description = request.form.get("description", "").strip()
    db.session.commit()
    flash("Skill updated.", "success")
    return redirect(url_for("admin.skills"))


@admin_bp.route("/skills/delete/<int:skill_id>", methods=["POST"])
@login_required
@admin_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    flash("Skill deleted.", "info")
    return redirect(url_for("admin.skills"))


# ---------------------------------------------------------------- CAREER-SKILL MAPPING
@admin_bp.route("/career-skills", methods=["GET", "POST"])
@login_required
@admin_required
def career_skills():
    if request.method == "POST":
        career_id = request.form.get("career_id")
        skill_id = request.form.get("skill_id")
        if not career_id or not skill_id:
            flash("Please select both a career and a skill.", "danger")
        elif CareerSkill.query.filter_by(career_id=career_id, skill_id=skill_id).first():
            flash("This skill is already mapped to this career.", "warning")
        else:
            db.session.add(CareerSkill(career_id=career_id, skill_id=skill_id))
            db.session.commit()
            flash("Skill mapped to career.", "success")
        return redirect(url_for("admin.career_skills"))

    all_careers = CareerRole.query.order_by(CareerRole.name).all()
    all_skills = Skill.query.order_by(Skill.name).all()
    mappings = CareerSkill.query.join(CareerRole).order_by(CareerRole.name).all()
    return render_template(
        "admin/career_skills.html", careers=all_careers, skills=all_skills, mappings=mappings
    )


@admin_bp.route("/career-skills/delete/<int:mapping_id>", methods=["POST"])
@login_required
@admin_required
def delete_career_skill(mapping_id):
    mapping = CareerSkill.query.get_or_404(mapping_id)
    db.session.delete(mapping)
    db.session.commit()
    flash("Mapping removed.", "info")
    return redirect(url_for("admin.career_skills"))


# ---------------------------------------------------------------- LEARNING RESOURCES
@admin_bp.route("/resources", methods=["GET", "POST"])
@login_required
@admin_required
def resources():
    if request.method == "POST":
        skill_id = request.form.get("skill_id")
        title = request.form.get("title", "").strip()
        provider = request.form.get("provider", "").strip()
        resource_type = request.form.get("resource_type", "").strip()
        level = request.form.get("level", "").strip()
        url_value = request.form.get("url", "").strip()
        description = request.form.get("description", "").strip()
        estimated_time = request.form.get("estimated_time", "").strip()
        is_verified = bool(request.form.get("is_verified"))
        is_active = bool(request.form.get("is_active"))

        errors = []
        if not skill_id or not title or not provider or not resource_type or not level or not url_value:
            errors.append("Please fill in all required fields.")
        if url_value and not (url_value.startswith("http://") or url_value.startswith("https://")):
            errors.append("URL must start with http:// or https://")

        if errors:
            for e in errors:
                flash(e, "danger")
        else:
            db.session.add(LearningResource(
                skill_id=skill_id, title=title, provider=provider,
                resource_type=resource_type, level=level, url=url_value,
                description=description, estimated_time=estimated_time,
                is_verified=is_verified, is_active=is_active,
            ))
            db.session.commit()
            flash("Resource added.", "success")
        return redirect(url_for("admin.resources"))

    all_resources = LearningResource.query.join(Skill).order_by(Skill.name, LearningResource.title).all()
    all_skills = Skill.query.order_by(Skill.name).all()
    resource_types = ["Course", "Video", "Documentation", "Article", "Practice", "Tutorial"]
    levels = ["Beginner", "Intermediate", "Advanced"]
    return render_template(
        "admin/resources.html", resources=all_resources, skills=all_skills,
        resource_types=resource_types, levels=levels,
    )


@admin_bp.route("/resources/edit/<int:resource_id>", methods=["POST"])
@login_required
@admin_required
def edit_resource(resource_id):
    r = LearningResource.query.get_or_404(resource_id)
    r.skill_id = request.form.get("skill_id", r.skill_id)
    r.title = request.form.get("title", r.title).strip()
    r.provider = request.form.get("provider", r.provider).strip()
    r.resource_type = request.form.get("resource_type", r.resource_type).strip()
    r.level = request.form.get("level", r.level).strip()
    r.url = request.form.get("url", r.url).strip()
    r.description = request.form.get("description", r.description or "").strip()
    r.estimated_time = request.form.get("estimated_time", r.estimated_time or "").strip()
    r.is_verified = bool(request.form.get("is_verified"))
    r.is_active = bool(request.form.get("is_active"))
    db.session.commit()
    flash("Resource updated.", "success")
    return redirect(url_for("admin.resources"))


@admin_bp.route("/resources/delete/<int:resource_id>", methods=["POST"])
@login_required
@admin_required
def delete_resource(resource_id):
    r = LearningResource.query.get_or_404(resource_id)
    db.session.delete(r)
    db.session.commit()
    flash("Resource deleted.", "info")
    return redirect(url_for("admin.resources"))


@admin_bp.route("/resources/toggle-active/<int:resource_id>", methods=["POST"])
@login_required
@admin_required
def toggle_resource_active(resource_id):
    r = LearningResource.query.get_or_404(resource_id)
    r.is_active = not r.is_active
    db.session.commit()
    flash(f"Resource is now {'active' if r.is_active else 'inactive'}.", "success")
    return redirect(url_for("admin.resources"))


@admin_bp.route("/resources/toggle-verified/<int:resource_id>", methods=["POST"])
@login_required
@admin_required
def toggle_resource_verified(resource_id):
    r = LearningResource.query.get_or_404(resource_id)
    r.is_verified = not r.is_verified
    db.session.commit()
    flash(f"Resource is now {'verified' if r.is_verified else 'unverified'}.", "success")
    return redirect(url_for("admin.resources"))


# ---------------------------------------------------------------- INTERVIEW QUESTIONS
@admin_bp.route("/interview-questions", methods=["GET", "POST"])
@login_required
@admin_required
def interview_questions():
    if request.method == "POST":
        career_id = request.form.get("career_id")
        question = request.form.get("question", "").strip()
        expected_keywords = request.form.get("expected_keywords", "").strip()

        if not career_id or not question or not expected_keywords:
            flash("Please fill in all fields.", "danger")
        else:
            db.session.add(InterviewQuestion(
                career_id=career_id, question=question, expected_keywords=expected_keywords
            ))
            db.session.commit()
            flash("Interview question added.", "success")
        return redirect(url_for("admin.interview_questions"))

    all_careers = CareerRole.query.order_by(CareerRole.name).all()
    all_questions = InterviewQuestion.query.join(CareerRole).order_by(CareerRole.name).all()
    return render_template("admin/interview_questions.html", careers=all_careers, questions=all_questions)


@admin_bp.route("/interview-questions/edit/<int:question_id>", methods=["POST"])
@login_required
@admin_required
def edit_interview_question(question_id):
    q = InterviewQuestion.query.get_or_404(question_id)
    q.career_id = request.form.get("career_id", q.career_id)
    q.question = request.form.get("question", q.question).strip()
    q.expected_keywords = request.form.get("expected_keywords", q.expected_keywords).strip()
    db.session.commit()
    flash("Question updated.", "success")
    return redirect(url_for("admin.interview_questions"))


@admin_bp.route("/interview-questions/delete/<int:question_id>", methods=["POST"])
@login_required
@admin_required
def delete_interview_question(question_id):
    q = InterviewQuestion.query.get_or_404(question_id)
    db.session.delete(q)
    db.session.commit()
    flash("Question deleted.", "info")
    return redirect(url_for("admin.interview_questions"))
