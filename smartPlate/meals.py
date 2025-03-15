# meals.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Meal
from flask_login import login_required, current_user

meals = Blueprint('meals', __name__)

@meals.route('/meals', methods=['GET', 'POST'])
@login_required
def log_meal():
    if request.method == 'POST':
        food_name = request.form['food_name']
        calories = request.form['calories']
        
        # Create a new meal entry
        new_meal = Meal(food_name=food_name, calories=calories, user_id=current_user.id)
        db.session.add(new_meal)
        db.session.commit()
        
        flash('Meal logged successfully!')
        return redirect(url_for('meals.log_meal'))
    
    # Fetch the user's meal entries
    meals = Meal.query.filter_by(user_id=current_user.id).all()
    return render_template('meals.html', meals=meals)