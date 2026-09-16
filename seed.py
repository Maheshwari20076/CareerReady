"""
Seed the CareerReady database with sample data for demonstration:
careers, skills, career-skill mappings, real-world learning resources,
interview questions, a demo admin account, and a demo student account.

Run with:  python seed.py
(Run this AFTER the MySQL database and tables have been created.)
"""

from app import create_app
from models import (
    db, User, StudentProfile, Skill, CareerRole, CareerSkill,
    LearningResource, InterviewQuestion, StudentSkill,
)

app = create_app()


def seed():
    with app.app_context():
        db.create_all()

        if User.query.first():
            print("Database already contains data. Skipping seed to avoid duplicates.")
            return

        # ---------------- SKILLS ----------------
        skill_names = [
            "Python", "SQL", "MySQL", "HTML", "CSS", "JavaScript", "Git",
            "Flask", "REST API", "Testing", "Excel", "Data Analysis",
            "Bootstrap", "React", "Java", "OOP", "Linux", "Communication",
        ]
        skills = {}
        for name in skill_names:
            s = Skill(name=name, description=f"{name} skill")
            db.session.add(s)
            skills[name] = s
        db.session.flush()

        # ---------------- CAREERS ----------------
        careers_data = {
            "Python Developer": "Build applications and backend systems using Python.",
            "Web Developer": "Design and build full websites using front-end and back-end technologies.",
            "Front-End Developer": "Build user interfaces using HTML, CSS, and JavaScript.",
            "Back-End Developer": "Build server-side logic, APIs, and databases.",
            "Data Analyst": "Analyze data to help businesses make informed decisions.",
            "Software Developer": "Design, build, and maintain software applications.",
            "SQL/Database Developer": "Design and manage relational databases.",
            "QA Tester": "Test software to find bugs and ensure quality.",
        }
        careers = {}
        for name, desc in careers_data.items():
            c = CareerRole(name=name, description=desc)
            db.session.add(c)
            careers[name] = c
        db.session.flush()

        # ---------------- CAREER SKILL MAPPINGS ----------------
        career_skill_map = {
            "Python Developer": ["Python", "SQL", "Git", "Flask", "REST API", "HTML", "CSS"],
            "Web Developer": ["HTML", "CSS", "JavaScript", "Bootstrap", "Git", "SQL"],
            "Front-End Developer": ["HTML", "CSS", "JavaScript", "React", "Bootstrap", "Git"],
            "Back-End Developer": ["Python", "SQL", "Flask", "REST API", "Git", "Linux"],
            "Data Analyst": ["Excel", "SQL", "Data Analysis", "Python", "Communication"],
            "Software Developer": ["Java", "OOP", "Git", "SQL", "Testing"],
            "SQL/Database Developer": ["SQL", "MySQL", "Data Analysis", "Excel"],
            "QA Tester": ["Testing", "SQL", "Communication", "Git"],
        }
        for career_name, skill_list in career_skill_map.items():
            for skill_name in skill_list:
                db.session.add(CareerSkill(career_id=careers[career_name].id, skill_id=skills[skill_name].id))
        db.session.flush()

        # ---------------- LEARNING RESOURCES (real, trusted URLs) ----------------
        resources_data = [
            # Python
            dict(skill="Python", title="Python Official Tutorial", provider="Python.org",
                 resource_type="Documentation", level="Beginner",
                 url="https://docs.python.org/3/tutorial/index.html",
                 description="The official beginner-friendly tutorial covering Python fundamentals.",
                 estimated_time="6 hours", is_verified=True),
            dict(skill="Python", title="Learn Python", provider="freeCodeCamp",
                 resource_type="Course", level="Beginner",
                 url="https://www.freecodecamp.org/learn/scientific-computing-with-python/",
                 description="A free, hands-on course covering Python programming basics.",
                 estimated_time="15 hours", is_verified=True),
            dict(skill="Python", title="Python Practice Problems", provider="HackerRank",
                 resource_type="Practice", level="Beginner",
                 url="https://www.hackerrank.com/domains/python",
                 description="Practice Python problems ranging from easy to hard.",
                 estimated_time="Self-paced", is_verified=True),
            dict(skill="Python", title="Python Tutorial", provider="W3Schools",
                 resource_type="Tutorial", level="Beginner",
                 url="https://www.w3schools.com/python/",
                 description="A beginner-friendly, example-driven Python tutorial.",
                 estimated_time="5 hours", is_verified=True),

            # SQL
            dict(skill="SQL", title="SQL Tutorial", provider="W3Schools",
                 resource_type="Tutorial", level="Beginner",
                 url="https://www.w3schools.com/sql/",
                 description="Learn SQL syntax and database queries step by step.",
                 estimated_time="6 hours", is_verified=True),
            dict(skill="SQL", title="Learn SQL", provider="freeCodeCamp",
                 resource_type="Course", level="Beginner",
                 url="https://www.freecodecamp.org/learn/relational-database/",
                 description="A free course covering relational databases and SQL.",
                 estimated_time="10 hours", is_verified=True),
            dict(skill="SQL", title="SQL Practice", provider="HackerRank",
                 resource_type="Practice", level="Intermediate",
                 url="https://www.hackerrank.com/domains/sql",
                 description="Practice writing SQL queries with real challenges.",
                 estimated_time="Self-paced", is_verified=True),

            # MySQL
            dict(skill="MySQL", title="MySQL Reference Manual", provider="MySQL.com",
                 resource_type="Documentation", level="Intermediate",
                 url="https://dev.mysql.com/doc/refman/8.0/en/",
                 description="The official MySQL documentation and reference manual.",
                 estimated_time="Reference", is_verified=True),
            dict(skill="MySQL", title="MySQL Tutorial", provider="W3Schools",
                 resource_type="Tutorial", level="Beginner",
                 url="https://www.w3schools.com/mysql/",
                 description="Learn to use MySQL with PHP and standalone examples.",
                 estimated_time="4 hours", is_verified=True),

            # HTML
            dict(skill="HTML", title="HTML Basics", provider="MDN Web Docs",
                 resource_type="Documentation", level="Beginner",
                 url="https://developer.mozilla.org/en-US/docs/Learn/HTML",
                 description="Mozilla's structured guide to learning HTML from scratch.",
                 estimated_time="8 hours", is_verified=True),
            dict(skill="HTML", title="HTML Tutorial", provider="W3Schools",
                 resource_type="Tutorial", level="Beginner",
                 url="https://www.w3schools.com/html/",
                 description="An interactive, example-based HTML tutorial.",
                 estimated_time="5 hours", is_verified=True),

            # CSS
            dict(skill="CSS", title="Learn CSS", provider="MDN Web Docs",
                 resource_type="Documentation", level="Beginner",
                 url="https://developer.mozilla.org/en-US/docs/Learn/CSS",
                 description="Mozilla's structured guide to CSS styling and layout.",
                 estimated_time="8 hours", is_verified=True),
            dict(skill="CSS", title="CSS Tutorial", provider="W3Schools",
                 resource_type="Tutorial", level="Beginner",
                 url="https://www.w3schools.com/css/",
                 description="An interactive, example-based CSS tutorial.",
                 estimated_time="5 hours", is_verified=True),

            # JavaScript
            dict(skill="JavaScript", title="JavaScript Guide", provider="MDN Web Docs",
                 resource_type="Documentation", level="Beginner",
                 url="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
                 description="Mozilla's comprehensive guide to the JavaScript language.",
                 estimated_time="10 hours", is_verified=True),
            dict(skill="JavaScript", title="JavaScript Algorithms and Data Structures", provider="freeCodeCamp",
                 resource_type="Course", level="Intermediate",
                 url="https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/",
                 description="A free, project-based JavaScript course.",
                 estimated_time="20 hours", is_verified=True),

            # Git
            dict(skill="Git", title="Introduction to Git", provider="GitHub Skills",
                 resource_type="Course", level="Beginner",
                 url="https://skills.github.com/",
                 description="Hands-on GitHub Skills courses covering Git and GitHub basics.",
                 estimated_time="3 hours", is_verified=True),
            dict(skill="Git", title="Git Documentation", provider="Git-scm.com",
                 resource_type="Documentation", level="Beginner",
                 url="https://git-scm.com/doc",
                 description="The official Git documentation and reference book.",
                 estimated_time="Reference", is_verified=True),
            dict(skill="Git", title="Git Tutorial", provider="W3Schools",
                 resource_type="Tutorial", level="Beginner",
                 url="https://www.w3schools.com/git/",
                 description="A beginner tutorial covering Git commands and workflow.",
                 estimated_time="3 hours", is_verified=True),

            # Flask
            dict(skill="Flask", title="Flask Documentation", provider="Flask (Pallets Projects)",
                 resource_type="Documentation", level="Intermediate",
                 url="https://flask.palletsprojects.com/",
                 description="The official Flask documentation with quick start and tutorials.",
                 estimated_time="6 hours", is_verified=True),
            dict(skill="Flask", title="Flask Tutorial", provider="GeeksforGeeks",
                 resource_type="Tutorial", level="Beginner",
                 url="https://www.geeksforgeeks.org/python/flask-tutorial/",
                 description="A step-by-step Flask tutorial for beginners.",
                 estimated_time="5 hours", is_verified=True),

            # REST API
            dict(skill="REST API", title="What is a REST API?", provider="Microsoft Learn",
                 resource_type="Article", level="Beginner",
                 url="https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design",
                 description="Microsoft's guide to designing and understanding REST APIs.",
                 estimated_time="1 hour", is_verified=True),
            dict(skill="REST API", title="REST API Tutorial", provider="freeCodeCamp",
                 resource_type="Tutorial", level="Beginner",
                 url="https://www.freecodecamp.org/news/what-is-an-api-in-english-please-b880a3214a82/",
                 description="A plain-English explanation of what APIs are and how REST works.",
                 estimated_time="1 hour", is_verified=True),

            # Testing
            dict(skill="Testing", title="Software Testing Tutorial", provider="GeeksforGeeks",
                 resource_type="Tutorial", level="Beginner",
                 url="https://www.geeksforgeeks.org/software-engineering/software-testing-basics/",
                 description="An introduction to software testing concepts and types.",
                 estimated_time="3 hours", is_verified=True),

            # Excel
            dict(skill="Excel", title="Excel Training", provider="Microsoft Learn",
                 resource_type="Course", level="Beginner",
                 url="https://support.microsoft.com/en-us/excel",
                 description="Official Microsoft Excel support and training hub.",
                 estimated_time="4 hours", is_verified=True),

            # Data Analysis
            dict(skill="Data Analysis", title="Data Analysis with Python", provider="freeCodeCamp",
                 resource_type="Course", level="Intermediate",
                 url="https://www.freecodecamp.org/learn/data-analysis-with-python/",
                 description="A free course covering data analysis using Python libraries.",
                 estimated_time="20 hours", is_verified=True),

            # Bootstrap
            dict(skill="Bootstrap", title="Bootstrap Documentation", provider="GetBootstrap.com",
                 resource_type="Documentation", level="Beginner",
                 url="https://getbootstrap.com/docs/5.3/getting-started/introduction/",
                 description="Official Bootstrap 5 documentation and components reference.",
                 estimated_time="4 hours", is_verified=True),

            # React
            dict(skill="React", title="React Quick Start", provider="React.dev",
                 resource_type="Documentation", level="Intermediate",
                 url="https://react.dev/learn",
                 description="The official React documentation and learning guide.",
                 estimated_time="10 hours", is_verified=True),

            # Java
            dict(skill="Java", title="Java Tutorial", provider="W3Schools",
                 resource_type="Tutorial", level="Beginner",
                 url="https://www.w3schools.com/java/",
                 description="A beginner-friendly, example-based Java tutorial.",
                 estimated_time="8 hours", is_verified=True),

            # OOP
            dict(skill="OOP", title="Object-Oriented Programming Concepts", provider="GeeksforGeeks",
                 resource_type="Article", level="Beginner",
                 url="https://www.geeksforgeeks.org/system-design/object-oriented-analysis-and-design/",
                 description="An overview of OOP principles: classes, objects, inheritance, and polymorphism.",
                 estimated_time="2 hours", is_verified=True),

            # Linux
            dict(skill="Linux", title="Linux Command Line Basics", provider="freeCodeCamp",
                 resource_type="Tutorial", level="Beginner",
                 url="https://www.freecodecamp.org/news/the-linux-commands-handbook/",
                 description="A handbook covering essential Linux terminal commands.",
                 estimated_time="4 hours", is_verified=True),

            # Communication
            dict(skill="Communication", title="Communication Skills for Interviews", provider="GeeksforGeeks",
                 resource_type="Article", level="Beginner",
                 url="https://www.geeksforgeeks.org/interview-experiences/tips-to-improve-communication-skills/",
                 description="Practical tips for improving verbal and written communication skills.",
                 estimated_time="1 hour", is_verified=True),
        ]

        for r in resources_data:
            db.session.add(LearningResource(
                skill_id=skills[r["skill"]].id,
                title=r["title"], provider=r["provider"], resource_type=r["resource_type"],
                level=r["level"], url=r["url"], description=r["description"],
                estimated_time=r["estimated_time"], is_verified=r["is_verified"], is_active=True,
            ))

        # ---------------- INTERVIEW QUESTIONS ----------------
        questions_data = {
            "Python Developer": [
                ("What is Python?", "python, interpreted, high-level, programming, language"),
                ("What are lists and tuples in Python?", "list, tuple, mutable, immutable, ordered"),
                ("What is a dictionary in Python?", "dictionary, key, value, pair, mapping"),
                ("What is OOP?", "object, class, inheritance, polymorphism, encapsulation"),
                ("What is Flask?", "flask, lightweight, web, framework, python"),
                ("What is a REST API?", "rest, api, http, endpoint, request, response"),
                ("What is SQL used for?", "sql, database, query, table, data"),
            ],
            "Web Developer": [
                ("What is HTML used for?", "html, markup, structure, webpage, elements"),
                ("What is CSS used for?", "css, style, layout, design, webpage"),
                ("What is responsive design?", "responsive, mobile, screen, layout, adapt"),
                ("What is Git used for?", "git, version, control, repository, commit"),
            ],
            "Data Analyst": [
                ("What does a data analyst do?", "data, analyze, insights, decisions, trends"),
                ("What is SQL used for in data analysis?", "sql, query, database, data, retrieve"),
                ("What is Excel used for?", "excel, spreadsheet, formula, data, analysis"),
            ],
            "QA Tester": [
                ("What is software testing?", "testing, bugs, quality, software, verify"),
                ("What is the difference between manual and automated testing?", "manual, automated, testing, script, tool"),
            ],
        }
        for career_name, qs in questions_data.items():
            for question_text, keywords in qs:
                db.session.add(InterviewQuestion(
                    career_id=careers[career_name].id, question=question_text, expected_keywords=keywords
                ))

        # ---------------- DEMO ACCOUNTS ----------------
        admin_user = User(name="Admin", email="admin@demo.com", role="admin")
        admin_user.set_password("admin123")
        db.session.add(admin_user)

        demo_student = User(name="Demo Student", email="student@demo.com", role="student")
        demo_student.set_password("student123")
        db.session.add(demo_student)
        db.session.flush()

        demo_profile = StudentProfile(
            user_id=demo_student.id, college="ABC College of Arts, Science & Commerce",
            degree="BCA", graduation_year=2027, location="Bengaluru",
            bio="BCA student exploring a career in Python development.",
            career_id=careers["Python Developer"].id,
        )
        db.session.add(demo_profile)

        # Demo student already knows Python, SQL, HTML, CSS (matches the example in the spec)
        for skill_name in ["Python", "SQL", "HTML", "CSS"]:
            db.session.add(StudentSkill(student_id=demo_student.id, skill_id=skills[skill_name].id))

        db.session.commit()
        print("Database seeded successfully!")
        print(" Admin login   -> admin@demo.com / admin123")
        print(" Student login -> student@demo.com / student123")


if __name__ == "__main__":
    seed()
