from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models import db, InterviewQuestion, InterviewAttempt
from utils import score_interview_answer, student_required

interview_bp = Blueprint("interview", __name__)


@interview_bp.route("/interview", methods=["GET"])
@login_required
@student_required
def interview():
    profile = current_user.profile
    career = profile.career if profile else None

    if not career:
        flash("Select a career first to practice career-specific interview questions.", "warning")
        return redirect(url_for("student.careers"))

    questions = InterviewQuestion.query.filter_by(career_id=career.id).all()

    latest_attempt = (
        InterviewAttempt.query.filter_by(student_id=current_user.id, career_id=career.id)
        .order_by(InterviewAttempt.created_at.desc())
        .first()
    )

    return render_template(
        "student/interview.html",
        career=career,
        questions=questions,
        latest_attempt=latest_attempt,
    )


@interview_bp.route("/interview/submit/<int:question_id>", methods=["POST"])
@login_required
@student_required
def submit_answer(question_id):
    question = InterviewQuestion.query.get_or_404(question_id)
    answer = request.form.get("answer", "").strip()

    score = score_interview_answer(answer, question.expected_keywords)

    attempt = InterviewAttempt(
        student_id=current_user.id,
        career_id=question.career_id,
        question_id=question.id,
        answer=answer,
        score=score,
    )
    db.session.add(attempt)
    db.session.commit()

    flash(f"Answer submitted. Your score: {score}%", "success")
    return redirect(url_for("interview.interview"))
