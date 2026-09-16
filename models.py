"""
Database models for CareerReady.

Each class maps directly to a MySQL table described in the project's
database design (see database/schema.sql for the equivalent raw SQL).
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")  # 'student' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship("StudentProfile", backref="user", uselist=False, cascade="all, delete-orphan")
    student_skills = db.relationship("StudentSkill", backref="student", cascade="all, delete-orphan")
    interview_attempts = db.relationship("InterviewAttempt", backref="student", cascade="all, delete-orphan")

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    @property
    def is_admin(self):
        return self.role == "admin"


class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    college = db.Column(db.String(200))
    degree = db.Column(db.String(100))
    graduation_year = db.Column(db.Integer)
    location = db.Column(db.String(150))
    bio = db.Column(db.Text)
    career_id = db.Column(db.Integer, db.ForeignKey("career_roles.id"), nullable=True)

    career = db.relationship("CareerRole", backref="students")


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))

    resources = db.relationship("LearningResource", backref="skill", cascade="all, delete-orphan")


class StudentSkill(db.Model):
    __tablename__ = "student_skills"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    skill = db.relationship("Skill")

    __table_args__ = (db.UniqueConstraint("student_id", "skill_id", name="uq_student_skill"),)


class CareerRole(db.Model):
    __tablename__ = "career_roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String(255))

    career_skills = db.relationship("CareerSkill", backref="career", cascade="all, delete-orphan")
    interview_questions = db.relationship("InterviewQuestion", backref="career", cascade="all, delete-orphan")


class CareerSkill(db.Model):
    __tablename__ = "career_skills"

    id = db.Column(db.Integer, primary_key=True)
    career_id = db.Column(db.Integer, db.ForeignKey("career_roles.id"), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.id"), nullable=False)

    skill = db.relationship("Skill")

    __table_args__ = (db.UniqueConstraint("career_id", "skill_id", name="uq_career_skill"),)


class LearningResource(db.Model):
    __tablename__ = "learning_resources"

    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    provider = db.Column(db.String(150), nullable=False)
    resource_type = db.Column(db.String(30), nullable=False)  # Course/Video/Documentation/Article/Practice/Tutorial
    level = db.Column(db.String(20), nullable=False)  # Beginner/Intermediate/Advanced
    url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500))
    estimated_time = db.Column(db.String(50))
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class InterviewQuestion(db.Model):
    __tablename__ = "interview_questions"

    id = db.Column(db.Integer, primary_key=True)
    career_id = db.Column(db.Integer, db.ForeignKey("career_roles.id"), nullable=False)
    question = db.Column(db.String(500), nullable=False)
    expected_keywords = db.Column(db.String(500), nullable=False)  # comma-separated
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class InterviewAttempt(db.Model):
    __tablename__ = "interview_attempts"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    career_id = db.Column(db.Integer, db.ForeignKey("career_roles.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("interview_questions.id"), nullable=False)
    answer = db.Column(db.Text)
    score = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    question = db.relationship("InterviewQuestion")
    career = db.relationship("CareerRole")
