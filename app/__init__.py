import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail  
from dotenv import load_dotenv


load_dotenv()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail() 
login_manager.login_view = 'main.login'

def create_app():
    app = Flask(__name__)

    # Get the URL
    database_url = os.getenv('DATABASE_URL')
    
    databaseConnectionSecure = False    
    # Check if it exists and fix the prefix
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)

        # try:
        #     app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        #     databaseConnectionSecure = True
        # except:
        #     print("Warning: DATABASE Operational Error, using SQLite fallback.")
            
    if not databaseConnectionSecure:
        # Fallback to local SQLite if DATABASE_URL is missing
        # This prevents the "Could not parse" crash
        database_url = 'sqlite:///portfolio.db'
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print("Warning: DATABASE_URL not found, using SQLite fallback.")
        
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-123')
    
    
    
    # Flask-Mail Configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS') # My 16-char App Password
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app) # Connect mail to app
    
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