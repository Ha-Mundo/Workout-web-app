from . import db
from .models import User
from .models import Workout
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required, logout_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/new')
@login_required
def new_workout():
    return render_template('create_workout.html')


@main.route('/new', methods=['POST'])
@login_required
def new_workout_post():
    exercise = request.form.get('exercise')
    sets = request.form.get('sets')
    reps = request.form.get('reps')
    notes = request.form.get('notes')

    workout = Workout(exercise=exercise, sets=sets, reps=reps, notes=notes, author=current_user)
    db.session.add(workout)
    db.session.commit()

    flash('Your exercise has been added!')

    return redirect(url_for('main.user_workouts'))


@main.route('/all')
@login_required
def user_workouts():
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    workouts = Workout.query.filter_by(author=user).paginate(page=page, per_page=6)
    return render_template('all_workouts.html', workouts=workouts, user=user)


@main.route("/workout/<int:workout_id>/update", methods=['GET', 'POST'])
@login_required
def update_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if request.method == 'POST':
        workout.exercise = request.form['exercise']
        workout.sets = request.form['sets']
        workout.reps = request.form['reps']
        workout.notes = request.form['notes']
        db.session.commit()
        flash('Your exercise has been updated!')
        return redirect(url_for('main.user_workouts'))
    return render_template('update_workout.html', workout=workout)


@main.route("/workout/<int:workout_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    flash('Your exercise has been deleted!')
    return redirect(url_for('main.user_workouts'))

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')