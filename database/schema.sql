-- CareerReady Database Schema (MySQL)
-- Import this file via phpMyAdmin (XAMPP) or run it with the mysql CLI.
-- Note: if you run the Flask app first, SQLAlchemy (db.create_all() inside
-- seed.py) will create these same tables automatically. This file is
-- provided so the schema can also be reviewed/imported independently.

CREATE DATABASE IF NOT EXISTS careerready CHARACTER SET utf8mb4;
USE careerready;

-- ---------------------------------------------------------------- users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'student',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------- career_roles
CREATE TABLE IF NOT EXISTS career_roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    description VARCHAR(255)
);

-- ---------------------------------------------------------------- student_profiles
CREATE TABLE IF NOT EXISTS student_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    phone VARCHAR(20),
    college VARCHAR(200),
    degree VARCHAR(100),
    graduation_year INT,
    location VARCHAR(150),
    bio TEXT,
    career_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (career_id) REFERENCES career_roles(id) ON DELETE SET NULL
);

-- ---------------------------------------------------------------- skills
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255)
);

-- ---------------------------------------------------------------- student_skills
CREATE TABLE IF NOT EXISTS student_skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    skill_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE,
    UNIQUE KEY uq_student_skill (student_id, skill_id)
);

-- ---------------------------------------------------------------- career_skills
CREATE TABLE IF NOT EXISTS career_skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    career_id INT NOT NULL,
    skill_id INT NOT NULL,
    FOREIGN KEY (career_id) REFERENCES career_roles(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE,
    UNIQUE KEY uq_career_skill (career_id, skill_id)
);

-- ---------------------------------------------------------------- learning_resources
CREATE TABLE IF NOT EXISTS learning_resources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    skill_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    provider VARCHAR(150) NOT NULL,
    resource_type VARCHAR(30) NOT NULL,
    level VARCHAR(20) NOT NULL,
    url VARCHAR(500) NOT NULL,
    description VARCHAR(500),
    estimated_time VARCHAR(50),
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);

-- ---------------------------------------------------------------- interview_questions
CREATE TABLE IF NOT EXISTS interview_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    career_id INT NOT NULL,
    question VARCHAR(500) NOT NULL,
    expected_keywords VARCHAR(500) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (career_id) REFERENCES career_roles(id) ON DELETE CASCADE
);

-- ---------------------------------------------------------------- interview_attempts
CREATE TABLE IF NOT EXISTS interview_attempts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    career_id INT NOT NULL,
    question_id INT NOT NULL,
    answer TEXT,
    score FLOAT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (career_id) REFERENCES career_roles(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES interview_questions(id) ON DELETE CASCADE
);
