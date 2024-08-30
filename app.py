from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from datetime import date
import os
import logging

from forms import UserAddForm, LoginForm, AddFoodForm, EditFoodForm, UserEditForm
from models import db, connect_db, User, FoodItem

logging.basicConfig(level=logging.DEBUG)

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

database_url = os.environ.get('DATABASE_URL', 'postgresql://lngzxeen:2696k2K-nG0m_I-GrAoRyayJtEJRqotY@kala.db.elephantsql.com/lngzxeen')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "BigBoyDeluxe")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['DEBUG'] = True

connect_db(app)

debug = DebugToolbarExtension(app)

API_KEY = os.environ.get('API_KEY', '2A3ZTZdTx5O5y605VbLnIxJoNnDB9BJhmnGxM0hy')

@app.before_request
def add_user_to_g():
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    session[CURR_USER_KEY] = user.id

def do_logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/')
def root():
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def add_user():
    if g.user:
        return redirect(f'/users/{g.user.id}')
    
    form = UserAddForm()
    if form.validate_on_submit():
        try:
            user = User.signup(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data,
                daily_calorie_goal=form.daily_calorie_goal.data
            )
            db.session.commit()
            app.logger.info(f"User created: {user.id}")
            do_login(user)
            app.logger.info(f"User logged in: {user.id}")
            return redirect(f'/users/{user.id}')
        except IntegrityError as e:
            db.session.rollback()
            app.logger.error(f"IntegrityError: {str(e)}")
            flash("Email already taken", 'danger')
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Unexpected error: {str(e)}")
            flash("An unexpected error occurred. Please try again.", 'danger')
    else:
        app.logger.info(f"Form validation failed: {form.errors}")
    
    return render_template('users/signup.html', form=form)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    if not g.user or g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.daily_calorie_goal = form.daily_calorie_goal.data

        db.session.commit()
        return redirect(f'/users/{user.id}')

    return render_template('users/edit.html', form=form, user=user)

@app.route('/login', methods=["GET", "POST"])
def login_user():
    if g.user:
        return redirect(f'/users/{g.user.id}')

    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(
            email=form.email.data,
            password=form.password.data
        )

        if user:
            do_login(user)
            flash("Logged in successfully!", "success")
            return redirect(f'/users/{user.id}')
        
        flash("Invalid credentials", "danger")
    
    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    do_logout()
    flash("Logged out successfully!", "success")
    return redirect('/login')

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    if not g.user or g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    today = date.today()
    return render_template('users/details.html', user=g.user, today=today)

@app.route('/get/food-items')
def get_food_items():
    date = request.args.get('date')
    food_items = FoodItem.query.filter_by(date=date, user_id=g.user.id)
    serialized_food_items = [{'id': item.id, 'meal_type': item.meal_type, 'item_name': item.item_name, 'calorie_total': item.calorie_total} for item in food_items]
    daily_calorie_goal = g.user.daily_calorie_goal if g.user else None

    return jsonify({'foodItems': serialized_food_items, 'user_id': g.user.id if g.user else None, 'daily_calorie_goal': daily_calorie_goal})

@app.route('/users/<int:user_id>/add_food', methods=['GET', 'POST'])
def AddFood(user_id):
    if not g.user or g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = AddFoodForm()
    user = User.query.get_or_404(user_id)

    if form.validate_on_submit():
        date_str = form.date.data.strftime('%Y-%m-%d')

        new_item = FoodItem(
            user_id=user_id,
            meal_type=form.meal_type.data,
            date=date_str,
            item_name=form.item_name.data,
            serving_size=form.serving_size.data,
            serving_measurement=form.serving_measurement.data,
            calorie_total=form.calorie_total.data,
            protein=form.protein.data,
            fat=form.fat.data,
            carb=form.carb.data
        )

        db.session.add(new_item)
        db.session.commit()

        return redirect(f'/users/{user_id}')
    
    return render_template('/food/addfood.html', form=form, user=user)

@app.route('/<int:user_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def EditFoodItem(user_id, item_id):
    if not g.user or g.user.id != user_id:
        flash("Access unauthorized", "danger")
        return redirect("/")
    
    form = EditFoodForm()
    user = User.query.get_or_404(user_id)
    item = FoodItem.query.get_or_404(item_id)

    if form.validate_on_submit():
        date_str = form.date.data.strftime('%Y-%m-%d')

        item.meal_type = form.meal_type.data
        item.date = date_str
        item.item_name = form.item_name.data
        item.serving_size = form.serving_size.data
        item.serving_measurement = form.serving_measurement.data
        item.calorie_total = form.calorie_total.data
        item.protein = form.protein.data
        item.fat = form.fat.data
        item.carb = form.carb.data

        db.session.commit()

        return redirect(f'/users/{user_id}')
    
    form.meal_type.data = item.meal_type
    form.date.data = item.date
    form.item_name.data = item.item_name
    form.serving_size.data = item.serving_size
    form.serving_measurement.data = item.serving_measurement
    form.calorie_total.data = item.calorie_total
    form.protein.data = item.protein
    form.fat.data = item.fat
    form.carb.data = item.carb

    return render_template('/food/editfood.html', form=form, user=user, item=item)

@app.route('/<int:user_id>/<int:item_id>/delete')
def delete_food_item(user_id, item_id):
    if not g.user or g.user.id != user_id:
        flash("Access unauthorized", "danger")
        return redirect("/")

    deleted_item = FoodItem.query.get_or_404(item_id)
    db.session.delete(deleted_item)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/test-db')
def test_db():
    try:
        db.session.execute('SELECT 1')
        return 'Database connection successful'
    except Exception as e:
        return f'Database connection failed: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)