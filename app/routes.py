from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "Welcome to the Activity Sharing App"

@main.route('/about')
def about():
    return "This is the about page."
