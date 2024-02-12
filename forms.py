from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length
from datetime import date

class UserAddForm(FlaskForm):
    """Form for adding users."""

    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    daily_calorie_goal = IntegerField('Daily Calorie Goal', validators=[DataRequired()])
    goal_weight = IntegerField('Goal Weight')

class UserEditForm(FlaskForm):
    """Form for adding users."""

    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=30)])
    daily_calorie_goal = IntegerField('Daily Calorie Goal', validators=[DataRequired()])
    goal_weight = IntegerField('Goal Weight')


class LoginForm(FlaskForm):
    """Form for adding Food Items."""

    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])

class AddFoodForm(FlaskForm):
    """Form for adding Food Items."""
    meal_choices = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Other', 'Other'),
    ]


    meal_type = SelectField('Meal Type', choices=meal_choices )
    date = DateField('Date', default=date.today)
    item_name = StringField('Food Item Name', validators=[DataRequired(), Length(min=1, max=100)])
    serving_size = IntegerField('Serving Size', validators=[DataRequired()])
    serving_measurement = StringField('Unit of Measurement')
    calorie_total = IntegerField('Calories', validators=[DataRequired()])
    protein = IntegerField('Protein (g)')
    fat = IntegerField('Fat (g)')
    carb = IntegerField('Carbohydrates (g)')

class EditFoodForm(FlaskForm):
    """Form for editing Food Items."""
    meal_choices = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Other', 'Other'),
    ]


    meal_type = SelectField('Meal Type', choices=meal_choices )
    date = DateField('Date', default=date.today)
    item_name = StringField('Food Item Name', validators=[DataRequired(), Length(min=1, max=100)])
    serving_size = IntegerField('Serving Size', validators=[DataRequired()])
    serving_measurement = StringField('Unit of Measurement')
    calorie_total = IntegerField('Calories', validators=[DataRequired()])
    protein = IntegerField('Protein (g)')
    fat = IntegerField('Fat (g)')
    carb = IntegerField('Carbohydrates (g)')
    