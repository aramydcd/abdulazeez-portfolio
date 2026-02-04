from datetime import datetime
from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_pic = db.Column(db.String(100), nullable=False, default='profile.jpg')
    status = db.Column(db.String(255), default="Open to Internships & Junior Roles")
    

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(200))
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    github_url = db.Column(db.String(200))
    live_demo_url = db.Column(db.String(200)) 
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
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    tools = db.Column(db.String(200))
    icon_class = db.Column(db.String(50), default='bi-code-slash')
    
class Experience(db.Model):
    __tablename__ = 'experiences'
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50))
    technologies = db.Column(db.String(200))
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    
class TargetRole(db.Model):
    __tablename__ = 'target_roles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    icon_class = db.Column(db.String(50), default='bi-cpu')
    description = db.Column(db.Text, nullable=False)
    cv_filename = db.Column(db.String(255), nullable=True)
    order = db.Column(db.Integer, default=0)
    
    
class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50))
    visit_time = db.Column(db.DateTime, default=datetime.utcnow)