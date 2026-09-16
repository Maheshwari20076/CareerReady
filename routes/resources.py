from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from models import LearningResource, Skill
from utils import calculate_skill_gap, student_required

resources_bp = Blueprint("resources", __name__)


@resources_bp.route("/resources")
@login_required
@student_required
def resources():
    profile = current_user.profile
    career = profile.career if profile else None

    gap = calculate_skill_gap(current_user.id, career.id if career else None) if career else None
    missing_skill_ids = [s.id for s in gap["missing"]] if gap else []

    # --- Recommended resources: active resources matching the student's missing skills ---
    recommended_by_skill = []
    if missing_skill_ids:
        for skill in gap["missing"]:
            skill_resources = (
                LearningResource.query.filter_by(skill_id=skill.id, is_active=True)
                .order_by(LearningResource.is_verified.desc(), LearningResource.title)
                .all()
            )
            if skill_resources:
                recommended_by_skill.append({"skill": skill, "resources": skill_resources})

    recommended_count = sum(len(group["resources"]) for group in recommended_by_skill)

    # --- Search + filters for "Explore All Resources" ---
    query_text = request.args.get("q", "").strip()
    skill_filter = request.args.get("skill", "").strip()
    type_filter = request.args.get("type", "").strip()
    level_filter = request.args.get("level", "").strip()
    sort_by = request.args.get("sort", "relevance").strip()

    q = LearningResource.query.filter_by(is_active=True)

    if query_text:
        like = f"%{query_text}%"
        q = q.join(Skill).filter(
            db_or(
                LearningResource.title.ilike(like),
                LearningResource.provider.ilike(like),
                LearningResource.description.ilike(like),
                Skill.name.ilike(like),
            )
        )

    if skill_filter:
        q = q.filter(LearningResource.skill_id == int(skill_filter))

    if type_filter:
        q = q.filter(LearningResource.resource_type == type_filter)

    if level_filter:
        q = q.filter(LearningResource.level == level_filter)

    if sort_by == "beginner":
        q = q.filter(LearningResource.level == "Beginner")
    elif sort_by == "verified":
        q = q.order_by(LearningResource.is_verified.desc(), LearningResource.title)
    elif sort_by == "shortest":
        q = q.order_by(LearningResource.estimated_time)
    else:
        q = q.order_by(LearningResource.title)

    all_resources = q.all()

    all_skills = Skill.query.order_by(Skill.name).all()
    resource_types = ["Course", "Video", "Documentation", "Article", "Practice", "Tutorial"]
    levels = ["Beginner", "Intermediate", "Advanced"]

    return render_template(
        "student/resources.html",
        career=career,
        gap=gap,
        recommended_by_skill=recommended_by_skill,
        recommended_count=recommended_count,
        all_resources=all_resources,
        all_skills=all_skills,
        resource_types=resource_types,
        levels=levels,
        query_text=query_text,
        skill_filter=skill_filter,
        type_filter=type_filter,
        level_filter=level_filter,
        sort_by=sort_by,
    )


def db_or(*conditions):
    from sqlalchemy import or_
    return or_(*conditions)
