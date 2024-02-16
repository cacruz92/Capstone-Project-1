from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from datetime import date



from forms import UserAddForm, LoginForm, AddFoodForm, EditFoodForm, UserEditForm
from models import db, connect_db, User, FoodItem

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///diet_tracker'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

with app.app_context():
    db.drop_all
    db.create_all()

app.config['SECRET_KEY'] = "BigBoyDeluxe"

app.config['DEBUG'] = True


debug = DebugToolbarExtension(app)

API_KEY = '2A3ZTZdTx5O5y605VbLnIxJoNnDB9BJhmnGxM0hy';

##############################################################################
# User signup/login/logout
##############################################################################

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global"""
    if CURR_USER_KEY in session:
        # g.user = User.query.get(session[CURR_USER_KEY])
        g.user = db.session.query(User).get(session[CURR_USER_KEY])


    else:
         g.user = None

def do_login(user):
     """Logs user in."""

     session[CURR_USER_KEY] = user.id

def do_logout():
     """Logs user out."""

     if CURR_USER_KEY in session:
          del session[CURR_USER_KEY]


@app.route('/')
def root():
    """Homepage"""
    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def add_user():
    """Handles the adding of a user"""

    if g.user:
        return redirect (f'/users/{g.user.id}')
    
    else:
        form = UserAddForm()

        if form.validate_on_submit():
            user = User.signup(
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                email = form.email.data,
                password = form.password.data,
                daily_calorie_goal = form.daily_calorie_goal.data,
                goal_weight = form.goal_weight.data
                )
            
            db.session.commit()
            
            do_login(user)

            return redirect(f'/users/{user.id}')

        else:
            return render_template('users/signup.html', form=form)
        
@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Handles the edit user form"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    elif g.user.id != user_id:
        flash("Access unauthorized: You can only view your own profile.", "danger")
        return redirect("/")
    
    else:
        user = User.query.get_or_404(user_id)
        form = UserEditForm(subj=user)

        if form.validate_on_submit():
                user.first_name = form.first_name.data,
                user.last_name = form.last_name.data,
                user.daily_calorie_goal = form.daily_calorie_goal.data,
                user.goal_weight = form.goal_weight.data

                db.session.commit()

                return redirect('/')

        else:
            form.first_name.data = user.first_name
            form.last_name.data = user.last_name
            form.daily_calorie_goal.data = user.daily_calorie_goal
            form.goal_weight.data = user.goal_weight

            return render_template('users/edit.html', form=form, user=user)

    
@app.route('/login', methods=["GET", "POST"])
def login_user():
    """Handles the logging in of a user"""

    if g.user:
        return redirect (f'/users/{g.user.id}')
    
    else:
        form = LoginForm()

        if form.validate_on_submit():
            user = User.authenticate(
                email = form.email.data,
                password = form.password.data
                )
            
            if user:
                do_login(user)
                flash("Logged in successfully!", "success")
                return redirect(f'/users/{user.id}')
            else:
                flash("Invalid credentials","danger")
        else:
            return render_template('users/login.html', form=form)
        
@app.route('/logout')
def logout():
    """Handle logout of user"""

    do_logout()
    flash("Logged out successfully!", "success")
    return redirect('/login')

    
@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    elif g.user.id != user_id:
        flash("Access unauthorized: You can only view your own profile.", "danger")
        return redirect("/")
    else:
        today = date.today()
        return render_template('users/details.html', user=g.user, today=today)

        

##############################################################################
# Adding/Editing/Deleting Food Routes
##############################################################################

@app.route('/get/food-items')
def get_food_items():
    date = request.args.get('date')
    food_items = FoodItem.query.filter_by(date=date)
    serialized_food_items = [{'id': item.id, 'meal_type': item.meal_type, 'item_name': item.item_name, 'calorie_total': item.calorie_total} for item in food_items]
    return jsonify({'foodItems': serialized_food_items, 'user_id': g.user.id if g.user else None})


@app.route('/users/<int:user_id>/add_food', methods=['GET', 'POST'])
def AddFood(user_id):
    """ add a food item"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    elif g.user.id != user_id:
        flash("Access unauthorized: You can only view your own profile.", "danger")
        return redirect("/")
    else:
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
        else:


            return render_template('/food/addfood.html', form=form, user=user)
        
@app.route('/<int:user_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def EditFoodItem(user_id, item_id):
    if not g.user:
        flash("Access unauthorized", "danger")

    elif g.user.id != user_id:
        flash("Access unauthorized: You can only view your own profile.", "danger")
        return redirect("/")
    else:
        form = EditFoodForm()
        user = User.query.get_or_404(user_id)
        item = FoodItem.query.get_or_404(item_id)

        if form.validate_on_submit():
            
            date_str = form.date.data.strftime('%Y-%m-%d')
            
            item.meal_type=form.meal_type.data,
            item.date=date_str,
            item.item_name=form.item_name.data,
            item.serving_size=form.serving_size.data,
            item.serving_measurement=form.serving_measurement.data,
            item.calorie_total=form.calorie_total.data,
            item.protein=form.protein.data,
            item.fat=form.fat.data,
            item.carb=form.carb.data

            db.session.commit()
            
            return redirect('/')
        else:
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
    deleted_item = FoodItem.query.get_or_404(item_id)
    db.session.delete(deleted_item)
    db.session.commit()

    return redirect(f'/users/{user_id}')

    
if __name__ == '__main__':
    app.run(debug=True)