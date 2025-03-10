import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import numpy as np
import pandas as pd
import joblib
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Ensure models directory exists
if not os.path.exists('models'):
    os.makedirs('models')

# Load dataset and train model (Only if model doesn't exist)
model_path = 'models/house_price_model.pkl'
if not os.path.exists(model_path):
    df = pd.read_csv("House Price India.csv")
    X = df[['living area', 'number of bedrooms', 'number of bathrooms']]
    y = df['Price']
    model = LinearRegression().fit(X, y)
    joblib.dump(model, model_path)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please login.', 'danger')
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        return redirect(url_for('dashboard'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('login'))

        session['user_id'] = user.id
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction_text = ""
    square_footage = ""
    bedrooms = ""
    bathrooms = ""

    if request.method == 'POST':
        square_footage = request.form['square_footage']
        bedrooms = request.form['bedrooms']
        bathrooms = request.form['bathrooms']

        if not square_footage or not bedrooms or not bathrooms:
            flash("Please fill in all fields!", "danger")
            return render_template('predict.html', prediction_text=prediction_text, 
                                   square_footage=square_footage, bedrooms=bedrooms, bathrooms=bathrooms)

        model = joblib.load('models/house_price_model.pkl')
        prediction = model.predict([[float(square_footage), int(bedrooms), float(bathrooms)]])[0]

        # Fix negative and zero price issue
        predicted_price = max(prediction, 10000)  # Minimum ₹10,000
        
        prediction_text = f'Estimated House Price: ₹{predicted_price:,.2f}'

    return render_template('predict.html', prediction_text=prediction_text, 
                           square_footage=square_footage, bedrooms=bedrooms, bathrooms=bathrooms)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
