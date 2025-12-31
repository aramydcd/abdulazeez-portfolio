from datetime import datetime
from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), default="Available for Internship")
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(200))  # e.g., "Python, Flask, Postgres"
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    github_url = db.Column(db.String(200))
    live_demo_url = db.Column(db.String(200)) # <--- Added this column
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Project('{self.title}', '{self.date_posted}')"

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    
class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False) # e.g., Backend
    description = db.Column(db.String(200))             # e.g., Architecting APIs...
    tools = db.Column(db.String(200))                   # e.g., Python, Flask, SQL
    icon_class = db.Column(db.String(50), default='bi-code-slash') # Bootstrap icon name
    
class Experience(db.Model):
    __tablename__ = 'experiences'
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100), nullable=False) # e.g., Software Developer Intern
    company = db.Column(db.String(100), nullable=False)   # e.g., 4Real Global IT Solution
    duration = db.Column(db.String(50))                  # e.g., Jan 2024 - April 2024
    description = db.Column(db.Text)                     # Key responsibilities/achievements
    order = db.Column(db.Integer, default=0)             # To control display sequence
    
class TargetRole(db.Model):
    __tablename__ = 'target_roles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) # e.g., Backend Developer
    icon_class = db.Column(db.String(50), default='bi-cpu') # Bootstrap icon name
    description = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, default=0)
    
class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50))
    visit_time = db.Column(db.DateTime, default=datetime.utcnow)