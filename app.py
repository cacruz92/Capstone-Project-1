from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm
from models import db, connect_db, User, FoodItem, Meal, DailyLog

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///diet_tracker'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

with app.app_context():
    # db.drop_all()
    db.create_all()

app.config['SECRET_KEY'] = "BigBoyDeluxe"

debug = DebugToolbarExtension(app)

@app.route('/')
def root():
    """Homepage"""
    return 'Welcome!'


if __name__ == '__main__':
    app.run(debug=True)