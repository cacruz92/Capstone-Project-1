Diet Diary Deluxe

- Description:
    The Diet Diary Deluxe app allows a user to make a profile. Then they can add food items they have consumed by name. The app will connect to the USDA Food API (https://fdc.nal.usda.gov/api-guide.html) and it retrieves the calorie and macronutrient information (carbohydrates, fat and protein). It takes all this information and stores it in a food item database table. With JavaScript, it then displays these items broken down by meal type (breakfast, lunch, dinner and other) and allows them to review daily food intake from today's date and past dates. It ill also show them how many calories they have left toward their daily calorie goal.

- Features Used:
    I used Flask, Jinja Templates, SQLAlchemy and Flask-WTForms and connected to a database. This allowed a user to register, adding their into a form that will be processed and added to a database. I also established a relationship between the users and food items tables so that a user can use a separate form to add food items to the database that are connected to that user. This way I was able to utilize JavaScript to access the food items belonging to this user to display on their profile page.  I also implemented password security with bcrypt.

- User Flow:  
    When a user first opens the app, they will be prompted to register, but the user will have the option to login below. The signup and login forms are implemented via Flask-WTForms. They both connect to a User model. The user information is saved to the database upon completion of the user registration. It also users a classmethod in the User Model to verify the login credentials. Once logged in, there is a profile that will show the user their personal information with their daily calorie goal. It also has a calendar select option that will allow them to select a date and see all the food that has been already logged on today's date and in the past. There is also a drop-down menu (accessible from every page) that will allow you to edit profile. This will generate the user edit form that will allow a user to change their information and goals. The user can also click on "add food" from the drop-down menu and this will generate the add food item form. They can select the date, the meal type and then type the food item name. Typing will access the API and it will provide a list of possible matching options. The user can then select with item matches their food or they can bypass the search and manually enter the information if the item is not found. It will redirect them to their profile where they can select today's date and see the entries. Their is a delete and edit button on each food item. These will allow a user to either remove the food entry or they can edit the name, meal type, date or macronutrients.

- API Used:
    https://fdc.nal.usda.gov/api-guide.html

- Technology Stack:
FrontEnd Development: HTML, JavaScript, CSS, Bootstrap, FontAwesome
BackEnd Development: Python
Framework: Flask (version 2.2.5)
Database: SQLAlchemy (version 2.0.25)
Database Driver: psycopg2-binary (version 2.9.9) - PostgreSQL adapter for Python.
ORM Extension: Flask-SQLAlchemy (version 3.0.5) 
Database Migration Tool: Flask-Migrate (version 4.0.5)
Security: Flask-Bcrypt (version 1.0.1)
Form Handling: WTForms (version 3.0.1)
Testing: Flask-Testing (version 0.8.1)
Debugging: Flask-DebugToolbar (version 0.14.1)
HTTP Request Handling: requests (version 2.31.0)
Templating: Jinja2 (version 3.1.3)

