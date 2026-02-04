import json
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
            admin = User(username='admin', password=hashed_pw, status="Open to Internships & Junior Entry Roles")
            db.session.add(admin)
            print("✅ Admin user created (User: admin, PW: admin123)")
        else:
            print("ℹ️ Admin user already exists. Skipping...")


        with open('datas.json', 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)

        projects = loaded_data["projects"]
        experiences = loaded_data["experiences"]
        skills = loaded_data["skills"]
        target_roles = loaded_data["target_roles"]
        
        # 3. Seed Projects (Check by title)
        project_titles = [pro["title"] for pro in projects]
        if not Project.query.filter(Project.title.in_(project_titles)).first():
            for pro in projects:
                new_project = Project(
                    title=pro["title"],
                    description=pro["description"],
                    technologies= pro["technologies"],
                    github_url=pro["github_url"],
                    live_demo_url = pro["live_demo_url"],
                    image_file=pro["image_file"]
                )
                db.session.add(new_project)
            print("✅ Projects seeded!")
        else:
            print("ℹ️ Projects already exist. Skipping...")

        # 4. Seed Skills (Check by category)
        if Skill.query.count() == 0:
            for skill in skills:
                new_skill = Skill(category=skill["category"], description=skill["description"], tools=skill["tools"], icon_class=skill["icon_class"])
                db.session.add(new_skill)
            print("✅ Skills seeded!")
        else:
            print("ℹ️ Skills already exist. Skipping...")

        # 5. Seed Experience
        if Experience.query.count() == 0:
            for exp in experiences:
                new_exp = Experience(
                    job_title=exp["job_title"],
                    company=exp["company"],
                    duration=exp["duration"],
                    technologies=exp["technologies"],
                    description=exp["description"]
                )
                db.session.add(new_exp)
            print("✅ Experience seeded!")

        # 6. Seed Target Roles
        if TargetRole.query.count() == 0:
            roles =[]
            for role in target_roles:
                new_role = TargetRole(title=role["title"], icon_class=role["icon_class"], description=role["description"], cv_filename= role.get("cv_filename", ""))
                
                roles.append(new_role)
                    
            db.session.add_all(roles)
            print("✅ Target Roles seeded!")

        db.session.commit()
        print("🚀 Seeding process complete!")


if __name__ == "__main__":
    seed_database()