from app import create_app, db
from app.models import User, Project, Skill, Experience, TargetRole
from werkzeug.security import generate_password_hash


app = create_app()

def seed_database():
    with app.app_context():
        # 1. Clear existing data
        print("Dropping and recreating all tables...")
        db.drop_all()
        db.create_all()

        # 2. Define sample projects
        p1 = Project(
            title="AI Chatbot",
            description="A real-time chatbot built with Flask and OpenAI API.",
            technologies="Python, Flask, OpenAI",
            github_url="https://github.com/aramydcde/chatbot",
            image_file="default.jpg"
        )
        
        p2 = Project(
            title="E-commerce Backend",
            description="A RESTful API for a clothing store with JWT authentication.",
            technologies="Python, PostgreSQL, Flask-JWT",
            github_url="https://github.com/aramydcd/shop-api",
            image_file="default.jpg"
        )

        # 3. Define the Technical Toolbox (Skills)
        s1 = Skill(
            category="Backend",
            description="Architecting secure APIs and logic using Python and Flask.",
            tools="Python, Flask, PostgreSQL",
            icon_class="bi-code-slash"
        )

        s2 = Skill(
            category="Frontend",
            description="Building responsive, user-first interfaces with modern CSS.",
            tools="HTML5, Bootstrap 5, JavaScript",
            icon_class="bi-layout-sidebar"
        )

        s3 = Skill(
            category="DevOps/Tools",
            description="Version control, deployment, and environment management.",
            tools="Git, UV, Docker",
            icon_class="bi-terminal"
        )

        # 4. Add all to database
        db.session.add_all([p1, p2, s1, s2, s3])
        db.session.commit()
        print("Database seeded with Projects and Skills!")
        
        # 5. Create Admin User
        hashed_pw = generate_password_hash('admin123', method='pbkdf2:sha256')
        admin = User(username='admin', password=hashed_pw, status="Open to Junior Entry Roles")
        
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully (User: admin, PW: admin123)")

        # 6. Define Work Experience
        e1 = Experience(
            job_title="Software Developer Intern (Backend Focus)",
            company="4Real Global IT Solution | Innovative ICT Firm",
            duration="Dec 2024 - Mar 2025",
            description="""
                • Financial Systems Optimization: Engineered high-precision server-side logic using VB.NET, reducing calculation latency by 15% for enterprise-level financial tools.\n
                • Scalable Architecture: Leveraged Object-Oriented Programming (OOP) to refactor legacy code into modular, reusable components, decreasing technical debt and future maintenance time.\n
                • SDLC Lifecycle Management: Actively contributed to the full Software Development Life Cycle, implementing rigorous debugging and unit testing protocols that improved system reliability by 20%.\n
                • Data Integrity & Security: Designed and maintained robust data structures for desktop service environments, ensuring 100% stability across multi-user financial transactions.\n
                • Cross-Functional Collaboration: Translated complex business requirements into technical specifications, bridging the gap between stakeholder needs and backend implementation.\n
            """
        )

        db.session.add(e1)
        db.session.commit()
        print("Experience seeded successfully!")

         # 7. Define Target Roles / Interests
        roles = [
            TargetRole(
                title="Backend Developer",
                icon_class="bi-server",
                description="Focused on building scalable server-side logic, API integrations, and database management using Python/Flask."
            ),
            TargetRole(
                title="Database Administrator",
                icon_class="bi-database-check",
                description="Interests in SQL optimization, data integrity, and designing efficient relational schemas for enterprise applications."
            ),
            TargetRole(
                title="Full-Stack Engineer",
                icon_class="bi-window-stack",
                description="Bridging the gap between robust backends and responsive frontends to create seamless user experiences."
            )
        ]

        db.session.add_all(roles)
        db.session.commit()
        print("Target Roles seeded successfully!")


if __name__ == "__main__":
    seed_database()