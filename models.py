from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import flask_bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

"""Models for Diet Tracker App"""

class User(db.Model):
    """User"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True
        )
    first_name = db.Column(
        db.String(30), 
        nullable=False
        )
    last_name = db.Column(
        db.String(30), 
        nullable=False
        )
    email = db.Column(
        db.String(50), 
        nullable=False
        )
    password = db.Column(
        db.String(50), 
        nullable=False
        )
    daily_calorie_goal = db.Column(
        db.Integer, 
        nullable=False
        )  
    goal_weight = db.Column(
        db.Integer, 
        nullable=True
        )
    
    def __repr__(self):
        return f"<User #{self.id}: {self.first_name} {self.last_name}, {self.email}>"
    
    @classmethod
    def signup(cls, email, password, first_name, last_name, daily_calorie_goal, goal_weight):
        """Sign up user
        
        Hashes password and adds to database
        """
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            first_name = first_name,
            last_name=last_name
            email=email
            password=hashed_pwd
            daily_calorie_goal=daily_calorie_goal
            goal_weight=goal_weight
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
            
        return False


class FoodItem(db.Model):
    """Meal"""

    __tablename__ = 'meals'

    id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True
        )
    meal_id = db.Column(
        db.Integer, 
        db.ForeignKey('meals.id')
        )
    serving_size = db.Column(
        db.String(30), 
        nullable=False
        )
    calorie_total = db.Column(
        db.Integer, 
        nullable=False
        )
    protein = db.Column(
        db.Integer, 
        nullable=True
        )
    fat = db.Column(
        db.Integer, 
        nullable=True
        )
    carb = db.Column(
        db.Integer, 
        nullable=True
        )


class Meal(db.Model):
    """Meal"""

    __tablename__ = 'meals'

    id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True
        )
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id')
        )
    date = db.Column(
        db.Date, 
        nullable=False
        )
    calorie_total = db.Column(
        db.Integer, 
        nullable=False
        )
    protein = db.Column(
        db.Integer, 
        nullable=True
        )
    fat = db.Column(
        db.Integer, 
        nullable=True
        )
    carb = db.Column(
        db.Integer, 
        nullable=True
        )


class DailyLog(db.Model):
    """Daily Log"""

    __tablename__ = 'logs'

    id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True
        )
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id')
        )   
    date = db.Column(
        db.Date, 
        nullable=False
        )
    calorie_total = db.Column(
        db.Integer, 
        nullable=False
        )
    protein = db.Column(
        db.Integer, 
        nullable=True
        )
    fat = db.Column(
        db.Integer, 
        nullable=True
        )
    carb = db.Column(
        db.Integer, 
        nullable=True
        )
    daily_weight = db.Column(
        db.Integer, 
        nullable=True
        )
    