from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm
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

def do_logout(user):
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
                print("User authenticated successfully.")
                print(f"User ID: {user.id}, Email: {user.email}")
                return redirect(f'/users/{user.id}')
            else:
                print("User authentication failed. Invalid email or password.")

        else:
            print("Form validation failed.")
            print("Form errors:", form.errors)

        # Render the login form template
        return render_template('users/login.html', form=form)

    
@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)

    return render_template('users/details.html', user=user)

            

if __name__ == '__main__':
    app.run(debug=True)