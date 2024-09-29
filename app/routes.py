from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Activity, Participation
from datetime import datetime
from . import db

main = Blueprint('main', __name__)

# Home page displaying upcoming activities
@main.route('/')
def index():
    activities = Activity.query.all()
    return render_template('index.html', activities=activities)

@main.route('/create', methods=['GET', 'POST'])
@login_required
def create_activity():
    if request.method == 'POST':
        activity_name = request.form.get('activity_name')
        description = request.form.get('description')
        date_str = request.form.get('date')
        time_str = request.form.get('time')  # New time field

        # Combine date and time into a datetime object
        date_time_str = f"{date_str} {time_str}"
        date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')  # Adjust format as needed

        new_activity = Activity(activity_name=activity_name, description=description, date_time=date_time, organizer_id=current_user.id)
        db.session.add(new_activity)
        db.session.commit()

        flash('Activity created successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template('create_activity.html')

# Route for users to join an activity
@main.route('/join/<int:activity_id>')
@login_required
def join_activity(activity_id):
    activity = Activity.query.get(activity_id)
    
    # Check if the activity exists
    if not activity:
        flash('Activity not found!', 'danger')
        return redirect(url_for('main.index'))
    
    # Check if the user has already joined the activity
    existing_participation = Participation.query.filter_by(user_id=current_user.id, activity_id=activity_id).first()
    if existing_participation:
        flash('You have already joined this activity.', 'info')
        return redirect(url_for('main.index'))

    # If not already joined, create a new participation record
    new_participation = Participation(user_id=current_user.id, activity_id=activity_id)
    db.session.add(new_participation)
    db.session.commit()

    flash(f'You have successfully joined the activity: {activity.activity_name}', 'success')
    return redirect(url_for('main.index'))

# User login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Login failed. Check your credentials.', 'danger')

    return render_template('login.html')

# User registration route
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

# User logout route
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Route to display user profile
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# Route to show activity details
@main.route('/activity/<int:activity_id>')
@login_required
def activity_detail(activity_id):
    activity = Activity.query.get(activity_id)
    return render_template('activity_detail.html', activity=activity)
