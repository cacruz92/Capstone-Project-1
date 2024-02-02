from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""Models for Diet Tracker App"""

class User(db.Model):
    """User"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    daily_calorie_goal = db.Column(db.Integer, nullable=False)
    goal_weight = db.Column(db.Integer, nullable=True)


class FoodItem(db.Model):
    """Meal"""

    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'))
    serving_size = db.Column(db.String(30), nullable=False)
    calorie_total = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=True)
    fat = db.Column(db.Integer, nullable=True)
    carb = db.Column(db.Integer, nullable=True)


class Meal(db.Model):
    """Meal"""

    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.Date, nullable=False)
    calorie_total = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=True)
    fat = db.Column(db.Integer, nullable=True)
    carb = db.Column(db.Integer, nullable=True)


class DailyLog(db.Model):
    """Daily Log"""

    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))   
    date = db.Column(db.Date, nullable=False)
    calorie_total = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=True)
    fat = db.Column(db.Integer, nullable=True)
    carb = db.Column(db.Integer, nullable=True)
    daily_weight = db.Column(db.Integer, nullable=True)