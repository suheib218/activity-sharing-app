from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize the database
db = SQLAlchemy()

# Initialize the login manager
login_manager = LoginManager()
login_manager.login_view = 'main.login'


# User model (make sure you have imported this in your code)
from .models import User

def create_app():
    app = Flask(__name__)
    
    # App configuration
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///activity_manager.db'
    
    # Initialize plugins
    db.init_app(app)
    login_manager.init_app(app)

    # Set the correct login view
    login_manager.login_view = 'main.login'

    # User loader for flask-login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register routes (blueprints will be defined later)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Create the database tables
    with app.app_context():
        db.create_all()

    return app

