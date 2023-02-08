from flask import Blueprint, flash, render_template, url_for, redirect, request
from flask_login import login_required, current_user
from .models import Workout
from .models import User 
from . import db


main = Blueprint('main', __name__)


# using decorators for routing
@main.route('/')
def index():
    # return 'Hello world!'
    # returning the rendered html pages instead

    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    # return 'Profile Here!'
    return render_template('profile.html', name=current_user.name)


# code for rendering the workouts
@main.route('/new')
@login_required
def new_workout():
    return render_template('create_workout.html')


# a function to handle the post request in the workout section
@main.route('/new', methods=['POST'])
@login_required
def new_workout_post():
    pushups = request.form.get('pushups')
    comment = request.form.get('comment')
    
    workout = Workout(pushups=pushups, comment=comment, author=current_user)

    db.session.add(workout)
    db.session.commit()

    flash('~Your workout has been added!')

    # redirecting to the page where all the workouts are stored for current user
    return redirect(url_for('main.user_workouts'))


# method to view all the data
@main.route('/all')
@login_required 
def user_workouts():
    user = User.query.filter_by(email = current_user.email).first_or_404()
    # this is because of the relational database we made with User and Workout
    workouts = user.workouts 

    # workouts_pagination = Workout.query.filter_by(author=user).paginate(per_page=2)
    # print(dir(workouts_pagination))
    # print(workouts_pagination.items)
    # print(workouts_pagination.pages)
    # print(workouts_pagination.page)
    # print(workouts_pagination.per_page)
    # print(workouts_pagination.total)
    flash('~~These are your workouts~~')

    return render_template('all_workouts.html', workouts=workouts, user=user)


# for updaing a specific workout with its ID, I have to also update the route path to it
@main.route('/workout/<int:workout_id>/update', methods=['GET', 'POST'])
@login_required 
def update_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)

    # if the form request is post, then I have to accept the values
    if request.method=='POST':
        workout.pushups = request.form['pushups']
        workout.comment = request.form['comment']

        db.session.commit()

        flash('~Your workout has been updated!')
        return redirect(url_for('main.user_workouts'))

    return render_template('update_workout.html', workout=workout)



# to delete a workout, just remove it from the db.session and again redirect the user to the all_workouts page
@main.route('/workout/<int:workout_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)

    db.session.delete(workout)
    db.session.commit()

    flash('~Your workout has been deleted!')

    return redirect(url_for('main.user_workouts'))


'''
    @ more about pagination
    but I don't mind doing it anymore
    whatever I have done till now is sufficient from visual point of view
'''