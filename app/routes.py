import os
import secrets
from flask import Blueprint, render_template, url_for, flash, redirect, request
from . import db
from .models import Project, User, Skill, Experience, TargetRole, Visitor
from .models import Message as MessageModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from flask import current_app
from sqlalchemy import func
from flask_mail import Message as MailMessage, Mail
from datetime import datetime, timedelta



main = Blueprint('main', __name__)

@main.app_errorhandler(404)
def page_not_found(e):
    # Note that we set the 404 status explicitly
    return render_template('404.html'), 404


@main.app_context_processor
def inject_last_updated():
    # Get the latest project date or experience date
    latest_project = db.session.query(func.max(Project.date_posted)).scalar()
    
    # Fallback date if database is empty
    display_date = latest_project.strftime("%B %d, %Y") if latest_project else "December 2025"
    
    return dict(last_updated=display_date)


# --- Login Route ---
@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')


@main.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))


@main.route("/")
@main.route("/home")
def home():
    projects = Project.query.order_by(Project.date_posted.desc()).limit(3).all()
    skills = Skill.query.all()
    experiences = Experience.query.order_by(Experience.id.desc()).all() 
    target_roles = TargetRole.query.order_by(TargetRole.order.asc()).all() 
    
    return render_template('index.html', 
                           projects=projects, 
                           skills=skills, 
                           experiences=experiences,
                           target_roles=target_roles)


@main.route("/projects")
def projects():
    # Look for a category in the URL (e.g., /projects?category=Python)
    category = request.args.get('category', 'all')
    projects = Project.query.order_by(Project.date_posted.desc()).all()
    return render_template('projects.html', projects=projects, active_category=category)


mail = Mail() # Initialize this in your app factory

@main.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # 1. Save to Database using the Model
        new_db_msg = MessageModel(
            name=name, 
            email=email, 
            subject=subject, 
            message=message
        )
        db.session.add(new_db_msg)
        db.session.commit()

        # 2. Send Email using MailMessage
        msg = MailMessage(
            subject=f"Portfolio: {subject}",
            sender='abdulakeem606@gmail.com',
            recipients=['abdulakeem606@gmail.com']
        )
        msg.body = f"Message from {name} ({email}):\n\n{message}"
        
        try:
            mail.send(msg)
            flash("Message sent successfully!", "success")
        except Exception as e:
            flash("Message saved, but email notification failed.", "warning")

        return redirect(url_for('main.contact'))
    return render_template('contact.html')


@main.route("/inbox")
@login_required
def inbox():
    # Fetch messages, newest first
    messages = MessageModel.query.order_by(MessageModel.timestamp.desc()).all()
    return render_template('inbox.html', messages=messages)

@main.route("/message/delete/<int:message_id>", methods=['POST'])
@login_required
def delete_message(message_id):
    msg = MessageModel.query.get_or_404(message_id)
    db.session.delete(msg)
    db.session.commit()
    flash('Message deleted.', 'info')
    return redirect(url_for('main.inbox'))


# --- ADD NEW PROJECT ---
def save_picture(form_picture):
    # Create a random hex name so users don't overwrite each other's images
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/img', picture_fn)
    
    # Save the file to the file system
    form_picture.save(picture_path)
    return picture_fn

@main.route("/project/new", methods=['GET', 'POST'])
@login_required
def new_project():
    if request.method == 'POST':
        # Handle Image
        image_file = 'default.jpg'
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                image_file = save_picture(file)
        
        project = Project(
            title=request.form.get('title'),
            description=request.form.get('description'),
            technologies=request.form.get('technologies'),
            github_url=request.form.get('github_url'),
            live_demo_url=request.form.get('live_demo_url'),
            image_file=image_file
        )
        
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('main.projects'))
        
    return render_template('project_form.html', title='New Project', project=None)


# --- UPDATE PROJECT DATA ---
@main.route("/project/<int:project_id>/update", methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        # If a new image is uploaded, process it
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                # Save new image and update field
                project.image_file = save_picture(file)
        
        # Update other fields
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.technologies = request.form.get('technologies')
        project.github_url = request.form.get('github_url')
        project.live_demo_url = request.form.get('live_demo_url')
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('main.project_detail', project_id=project.id))
        
    return render_template('project_form.html', title='Update Project', project=project)


# --- DELETE PROJECT ---
@main.route("/project/<int:project_id>/delete", methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted!', 'info')
    return redirect(url_for('main.home'))

@main.route("/project/<int:project_id>")
def project_detail(project_id):
    # .get_or_404 is great because it automatically returns a 404 page if the ID is wrong
    project = Project.query.get_or_404(project_id)
    return render_template('project_detail.html', project=project)

@main.route("/skill/new", methods=['GET', 'POST'])
@login_required
def new_skill():
    if request.method == 'POST':
        skill = Skill(
            category=request.form.get('category'),
            description=request.form.get('description'),
            tools=request.form.get('tools'),
            icon_class=request.form.get('icon_class')
        )
        db.session.add(skill)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('skill_form.html')

@main.route("/manage-skills")
@login_required
def manage_skills():
    skills = Skill.query.all()
    return render_template('manage_skills.html', skills=skills)

@main.route("/skill/delete/<int:skill_id>", methods=['POST'])
@login_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill category removed.', 'info')
    return redirect(url_for('main.manage_skills'))

@main.route("/skill/edit/<int:skill_id>", methods=['GET', 'POST'])
@login_required
def edit_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if request.method == 'POST':
        skill.category = request.form.get('category')
        skill.description = request.form.get('description')
        skill.tools = request.form.get('tools')
        skill.icon_class = request.form.get('icon_class')
        db.session.commit()
        flash('Skill updated!', 'success')
        return redirect(url_for('main.manage_skills'))
    return render_template('skill_form.html', skill=skill, title="Update Skill")

@main.route("/manage-experience")
def manage_experience():
    experiences = Experience.query.order_by(Experience.order.asc()).all()
    return render_template('manage_experience.html', experiences=experiences)

@main.route("/experience/new", methods=['GET', 'POST'])
@login_required
def new_experience():
    if request.method == 'POST':
        exp = Experience(
            job_title=request.form.get('job_title'),
            company=request.form.get('company'),
            duration=request.form.get('duration'),
            description=request.form.get('description')
        )
        db.session.add(exp)
        db.session.commit()
        flash('Experience added!', 'success')
        return redirect(url_for('main.manage_experience'))
    return render_template('experience_form.html', title="Add Experience")

@main.route("/experience/delete/<int:exp_id>", methods=['POST'])
@login_required
def delete_experience(exp_id):
    exp = Experience.query.get_or_404(exp_id)
    db.session.delete(exp)
    db.session.commit()
    flash('Experience record deleted.', 'info')
    return redirect(url_for('main.manage_experience'))

@main.route("/experience/edit/<int:exp_id>", methods=['GET', 'POST'])
@login_required
def edit_experience(exp_id):
    exp = Experience.query.get_or_404(exp_id)
    if request.method == 'POST':
        exp.job_title = request.form.get('job_title')
        exp.company = request.form.get('company')
        exp.duration = request.form.get('duration')
        exp.description = request.form.get('description')
        
        db.session.commit()
        flash('Experience updated successfully!', 'success')
        return redirect(url_for('main.manage_experience'))
    return render_template('experience_form.html', exp=exp, title="Update Experience")


@main.route("/role/new", methods=['GET', 'POST'])
@login_required
def new_role():
    if request.method == 'POST':
        role = TargetRole(
            title=request.form.get('title'),
            icon_class=request.form.get('icon_class'),
            description=request.form.get('description')
        )
        db.session.add(role)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('role_form.html', title="Add Target Role")


@main.route("/role/edit/<int:role_id>", methods=['GET', 'POST'])
@login_required
def edit_role(role_id):
    role = TargetRole.query.get_or_404(role_id)
    if request.method == 'POST':
        role.title = request.form.get('title')
        role.icon_class = request.form.get('icon_class')
        role.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('role_form.html', role=role, title="Edit Role")


@main.route("/role/delete/<int:role_id>", methods=['POST'])
@login_required
def delete_role(role_id):
    role = TargetRole.query.get_or_404(role_id)
    db.session.delete(role)
    db.session.commit()
    flash('Target role has been removed.', 'info')
    return redirect(url_for('main.home'))


@main.route("/update-status", methods=['POST'])
@login_required
def update_status():
    new_status = request.form.get('status')
    current_user.status = new_status
    db.session.commit()
    flash('Status updated!', 'success')
    return redirect(url_for('main.home'))


# @main.before_app_request
# def track_visitor():
#     # Only track if it's not the admin or a static file request
#     if not request.path.startswith('/static') and not current_user.is_authenticated:
#         visit = Visitor(ip_address=request.remote_addr)
#         db.session.add(visit)
#         db.session.commit()
        
        
# @main.route("/dashboard")
# @login_required
# def dashboard():
#     # Get total visits
#     total_visits = Visitor.query.count()
#     # Get visits from the last 24 hours
#     recent_visits = Visitor.query.filter(Visitor.visit_time > datetime.utcnow() - timedelta(days=1)).count()
    
#     return render_template('dashboard.html', 
#                            total_visits=total_visits, 
#                            recent_visits=recent_visits)
    
    
@main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        user = current_user
        
        # Update Username
        new_username = request.form.get('username')
        if new_username:
            user.username = new_username
            
        # Update Password (only if provided)
        new_password = request.form.get('password')
        if new_password:
            user.password = generate_password_hash(new_password)
            
        db.session.commit()
        flash('Settings updated successfully!')
        return redirect(url_for('main.settings'))
        
    return render_template('settings.html')