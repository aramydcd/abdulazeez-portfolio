import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail  # 1. New Import
from dotenv import load_dotenv

# Extensions defined outside the factory
load_dotenv()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail() # 2. Initialize Mail Extension
login_manager.login_view = 'main.login'

def create_app():
    app = Flask(__name__)
    
    # 3. Enhanced Configuration
    uri = os.getenv('DATABASE_URL', 'sqlite:///portfolio.db')
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-123')
    
    # 4. Flask-Mail Configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS') # Your 16-char App Password
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app) # 5. Connect mail to app
    
    # IMPORT AND REGISTER 
    from .models import User  # Moved inside to avoid circular imports
    from .routes import main
    app.register_blueprint(main)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    with app.app_context():
        db.create_all()
        
    return app