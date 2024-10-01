from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Activity, Participation
from datetime import datetime
from . import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

main = Blueprint('main', __name__)

# User registration form
class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(max=100)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(max=100)])
    mobilenumber = StringField('Mobile Number', validators=[DataRequired(), Length(max=15)])
    username = StringField('Username', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    street = StringField('Street', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Register')

# Home page displaying upcoming activities
@main.route('/')
def index():
    activities = Activity.query.all()  # Fetch all activities
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
        date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')

        new_activity = Activity(activity_name=activity_name, description=description, date_time=date_time, organizer_id=current_user.id)
        db.session.add(new_activity)
        db.session.commit()

        flash('Activity created successfully!', 'success')
        return redirect(url_for('main.activities'))

    return render_template('create_activity.html')

# Route for users to join an activity
@main.route('/join/<int:activity_id>', methods=['GET', 'POST'])
@login_required
def join_activity(activity_id):
    activity = Activity.query.get(activity_id)
    
    if not activity:
        flash('Activity not found!', 'danger')
        return redirect(url_for('main.index'))
    
    existing_participation = Participation.query.filter_by(user_id=current_user.id, activity_id=activity_id).first()
    if existing_participation:
        flash('You have already joined this activity.', 'info')
        return redirect(url_for('main.activities'))

    new_participation = Participation(user_id=current_user.id, activity_id=activity_id)
    db.session.add(new_participation)
    db.session.commit()

    flash(f'You have successfully joined the activity: {activity.activity_name}', 'success')
    return redirect(url_for('main.activities'))

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

# User registration route (no password hashing)
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Save plain text password
        new_user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            mobilenumber=form.mobilenumber.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,  # Save plain text password
            country=form.country.data,
            city=form.city.data,
            street=form.street.data
        )

      
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)

# User logout route
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# Route to display user profile
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# Route to show activity details
@main.route('/activity/<int:activity_id>')
def activity_detail(activity_id):
    activity = Activity.query.get(activity_id)
    if not activity:
        flash('Activity not found!', 'danger')
        return redirect(url_for('main.index'))
    return render_template('activity_detail.html', activity=activity)

@main.route('/activities')
@login_required
def activities():
    activities = Activity.query.all()
    user_participation = [p.activity_id for p in Participation.query.filter_by(user_id=current_user.id).all()]
    return render_template('activities.html', activities=activities, user_participation=user_participation)

@main.route('/activities/<int:activity_id>/update', methods=['GET', 'POST'])
@login_required
def update_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)

    if activity.organizer_id != current_user.id:
        flash("You are not authorized to update this activity.", "danger")
        return redirect(url_for('main.activities'))

    if request.method == 'POST':
        activity.activity_name = request.form['activity_name']
        activity.description = request.form['description']
        activity.date_time = f"{request.form['date']} {request.form['time']}"
        db.session.commit()
        flash("Activity updated successfully!", "success")
        return redirect(url_for('main.activities'))

    return render_template('update_activity.html', activity=activity)

@main.route('/activities/<int:activity_id>/delete', methods=['POST'])
@login_required
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)

    if activity.organizer_id != current_user.id:
        flash("You are not authorized to delete this activity.", "danger")
        return redirect(url_for('main.activities'))

    db.session.delete(activity)
    db.session.commit()
    flash("Activity deleted successfully!", "success")
    return redirect(url_for('main.activities'))

# Route to view a participant's profile
@main.route('/user/<int:user_id>')
@login_required
def view_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    activities_joined = Participation.query.filter_by(user_id=user.id).all()
    return render_template('participant_profile.html', user=user, activities_joined=activities_joined)
