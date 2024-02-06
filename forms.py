from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length

class UserAddForm(FlaskForm):
    """Form for adding users."""

    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    daily_calorie_goal = IntegerField('Daily Calorie Goal', validators=[DataRequired()])
    goal_weight = IntegerField('Goal Weight')


class LoginForm(FlaskForm):
    """Form for adding Food Items."""

    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])

class AddFoodForm(FlaskForm):
    """Form for adding Food Items."""

    meal = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
