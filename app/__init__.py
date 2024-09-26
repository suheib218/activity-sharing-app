from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize the database
db = SQLAlchemy()

# Initialize the login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

    # Initialize plugins
    db.init_app(app)
    login_manager.init_app(app)

    # Register routes (blueprints will be defined later)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
