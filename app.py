from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm, AddFoodForm
from models import db, connect_db, User, FoodItem, DailyLog

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///diet_tracker'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///diet_tracker?options=-csearch_path%3Ddiet_tracker'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

with app.app_context():
    db.drop_all
    db.create_all()

app.config['SECRET_KEY'] = "BigBoyDeluxe"

debug = DebugToolbarExtension(app)

##############################################################################
# User signup/login/logout
##############################################################################

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global"""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
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
                return redirect(f'/users/{user.id}')
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
        return render_template('users/details.html', user=g.user)

        

##############################################################################
# Adding Food Routes
##############################################################################

@app.route('/users/<int:user_id>/add_food', methods=['GET', 'POST'])
def AddFood(user_id):
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
                user_id = user_id,
                meal_type = form.meal_type.data,
                date = date_str,
                item_name = form.item_name.data,
                serving_size = form.serving_size.data,
                calorie_total = form.calorie_total.data,
                protein = form.protein.data,
                fat = form.fat.data,
                carb = form.carb.data
            )

            db.session.add(new_item)
            db.session.commit()

            return redirect(f'/users/{user_id}')
        else:
            return render_template('/users/addfood.html', form=form, user=user)


if __name__ == '__main__':
    app.run(debug=True)