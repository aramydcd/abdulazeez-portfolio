from app import create_app, db
from app.models import User, Project, Skill, Experience, TargetRole
from werkzeug.security import generate_password_hash

app = create_app()

def seed_database():
    with app.app_context():
        # 1. Initialize Tables (Create if they don't exist, but don't drop them)
        print("Ensuring tables exist...")
        db.create_all()

        # 2. Seed Admin User
        admin_exists = User.query.filter_by(username='admin').first()
        if not admin_exists:
            hashed_pw = generate_password_hash('admin123', method='pbkdf2:sha256')
            admin = User(username='admin', password=hashed_pw, status="Open to Junior Entry Roles")
            db.session.add(admin)
            print("✅ Admin user created (User: admin, PW: admin123)")
        else:
            print("ℹ️ Admin user already exists. Skipping...")

        # 3. Seed Projects (Check by title)
        project_titles = ["AI Chatbot", "E-commerce Backend"]
        if not Project.query.filter(Project.title.in_(project_titles)).first():
            p1 = Project(
                title="AI Chatbot",
                description="A real-time chatbot built with Flask and OpenAI API.",
                technologies="Python, Flask, OpenAI",
                github_url="https://github.com/aramydcd/chatbot",
                image_file="default.jpg"
            )
            p2 = Project(
                title="E-commerce Backend",
                description="A RESTful API for a clothing store with JWT authentication.",
                technologies="Python, PostgreSQL, Flask-JWT",
                github_url="https://github.com/aramydcd/shop-api",
                image_file="default.jpg"
            )
            db.session.add_all([p1, p2])
            print("✅ Projects seeded!")
        else:
            print("ℹ️ Projects already exist. Skipping...")

        # 4. Seed Skills (Check by category)
        if Skill.query.count() == 0:
            s1 = Skill(category="Backend", description="Architecting secure APIs and logic using Python and Flask.", tools="Python, Flask, PostgreSQL", icon_class="bi-code-slash")
            s2 = Skill(category="Frontend", description="Building responsive, user-first interfaces with modern CSS.", tools="HTML5, Bootstrap 5, JavaScript", icon_class="bi-layout-sidebar")
            s3 = Skill(category="DevOps/Tools", description="Version control, deployment, and environment management.", tools="Git, UV, Docker", icon_class="bi-terminal")
            db.session.add_all([s1, s2, s3])
            print("✅ Skills seeded!")
        else:
            print("ℹ️ Skills already exist. Skipping...")

        # 5. Seed Experience
        if Experience.query.count() == 0:
            e1 = Experience(
                job_title="Software Developer Intern (Backend Focus)",
                company="4Real Global IT Solution | Innovative ICT Firm",
                duration="Dec 2024 - Mar 2025",
                description="""• Financial Systems Optimization: Engineered high-precision logic..."""
            )
            db.session.add(e1)
            print("✅ Experience seeded!")

        # 6. Seed Target Roles
        if TargetRole.query.count() == 0:
            roles = [
                TargetRole(title="Backend Developer", icon_class="bi-server", description="Focused on building scalable server-side logic..."),
                TargetRole(title="Database Administrator", icon_class="bi-database-check", description="Interests in SQL optimization..."),
                TargetRole(title="Full-Stack Engineer", icon_class="bi-window-stack", description="Bridging the gap between backends and frontends...")
            ]
            db.session.add_all(roles)
            print("✅ Target Roles seeded!")

        db.session.commit()
        print("🚀 Seeding process complete!")

if __name__ == "__main__":
    seed_database()