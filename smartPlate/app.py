# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db, login_manager
from models import User, Favorite, Meal
from auth import auth
from nutritionix_api import get_nutritional_info
from clarifai_food_model import predict_food_items, initialize_clarifai_client
import os
from werkzeug.utils import secure_filename


# Initialize Flask app
app = Flask(__name__)

# ✅ MySQL Database Configuration (Update with your credentials)
DB_USERNAME = "root"
DB_PASSWORD = "root"
DB_HOST = "localhost"  # Example: 'localhost' for local MySQL, or cloud hostname
DB_NAME = "meal_tracker"

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)

# Initialize Clarifai client
API_KEY = "0aad4025c94e4b61b1717ae7af7d759b"  # Replace with your Clarifai API key
stub, metadata = initialize_clarifai_client(API_KEY)

# Register Blueprints
app.register_blueprint(auth, url_prefix='/auth')

# Routes
@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/nutrix', methods=['GET', 'POST'])
@login_required
def nutrix():
    nutritional_info = None
    query = None
    if request.method == 'POST':
        query = request.form.get('food_query')
        if query:
            nutritional_info = get_nutritional_info(query)
    return render_template('nutrix.html', nutritional_info=nutritional_info, query=query)

@app.route('/image_recognition', methods=['GET', 'POST'])
@login_required
def image_recognition():
    food_items = None
    image_path = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename:
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)
            food_items = predict_food_items(stub, metadata, image_path)
    return render_template('index.html', food_items=food_items, image_path=image_path)

@app.route('/meals', methods=['GET', 'POST'])
@login_required
def meals():
    if request.method == 'POST':
        food_name = request.form['food_name']
        calories = request.form['calories']
        new_meal = Meal(food_name=food_name, calories=calories, user_id=current_user.id)
        db.session.add(new_meal)
        db.session.commit()
        flash('Meal logged successfully!')
        return redirect(url_for('meals'))
    meals = Meal.query.filter_by(user_id=current_user.id).all()
    return render_template('meals.html', meals=meals)

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.drop_all()  # Drop all tables
        db.create_all()  # Recreate tables with the updated schema
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)