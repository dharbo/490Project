from flask import Flask, render_template, request, redirect, abort, flash

import sqlite3
import uuid
# import time

# Set up the database
DATABASE = './database.db'

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS USER (User_Name TEXT PRIMARY KEY, Password TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS CATEGORY (Category_Name TEXT, User_Name TEXT, Budget_Amount TEXT, FOREIGN KEY (User_Name) REFERENCES USER (User_Name), PRIMARY KEY (Category_Name, User_Name))")
cursor.execute("CREATE TABLE IF NOT EXISTS TRANSACTIONS (Transaction_ID TEXT, Category_Name TEXT, User_Name TEXT, Description TEXT, Money_Spent TEXT, FOREIGN KEY (User_Name) REFERENCES USER (User_Name), FOREIGN KEY (Category_Name) REFERENCES CATEGORY (Category_Name), PRIMARY KEY (Transaction_ID, Category_Name, User_Name))")

## TESTING with transactions
cursor.execute("INSERT OR IGNORE INTO TRANSACTIONS VALUES (?,?,?,?,?)", ('2','Insurance','david','AAA','200'))
connection.commit()
##

connection.close()

### Need a way to check if a user is logged in. If they aren't they shouldn't be able to access the home page
user_logged_in = ("", False)

app = Flask('__name__')

app.config['SECRET_KEY'] = uuid.uuid4().hex

def get_category_data():

    category_data = dict()

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    category_rows = cursor.execute("SELECT * FROM CATEGORY WHERE User_Name=?", (user_logged_in[0],)).fetchall()

    for category_row in category_rows:
        transactions_for_category = dict()

        transactions_rows = cursor.execute("SELECT * FROM TRANSACTIONS WHERE User_Name=? AND Category_Name=?", (user_logged_in[0],category_row[0],)).fetchall()
        for transactions_row in transactions_rows:
            transactions_for_category[f'{transactions_row[0]}'] = {'Description':f'{transactions_row[3]}',
                                                                    'Money_Spent':f'{transactions_row[4]}'}
            
        category_data[f'{category_row[0]}'] = transactions_for_category

    connection.close()

    return {'User_Name':f'{user_logged_in[0]}', 'Category_Data':f'{category_data}'}

@app.route('/')
def index():
    return render_template('index.html', title='Landing Page')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == 'POST':

        # Get the data from the form
        username = request.form.get('username')
        password = request.form.get('password')

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        row = cursor.execute("SELECT User_Name FROM USER WHERE User_Name=?", (username,)).fetchone()

        # If row does not exist in the database, insert the data. Otherwise make the user retry.
        if row is None:
            cursor.execute("INSERT INTO USER VALUES (?, ?)", (username, password,))
            connection.commit()
            connection.close()
            global user_logged_in
            user_logged_in = (username, True)
            return redirect('home')

        else:
            connection.close()
            return render_template('signup.html', title='Signup', retry=True)
    
    return render_template('signup.html', title='Signup')  # This is a get, should there be an if statement?

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':

        # Get the data from the form
        username = request.form.get('username')
        password = request.form.get('password')

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        row = cursor.execute("SELECT User_Name, Password FROM USER WHERE User_Name=? AND Password=?", (username, password,)).fetchone()

        # If row exists, then user successfully logged in. Otherwise, the inputted username or password was incorrect.
        if row is not None:
            global user_logged_in
            user_logged_in = (username, True)
            connection.close()


            return redirect('/home')

        else:
            connection.close()
            return render_template('login.html', title='Login', retry=True)

    return render_template('login.html', title='Login')  # This is a get, should there be an if statement?

@app.route('/home')
def home():
    # This should only be accessed by users who are logged in.
    if user_logged_in[1]:
        user_expense_data = get_category_data() # continue from here

        return render_template('home.html', title='Home', homepage="true")
    else:
        abort(403)

@app.route('/home/create-category', methods=["POST"])
def createCategory():

    categoryName = request.form.get('category-name')
    budget = request.form.get('budget')

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    row = cursor.execute("SELECT * FROM CATEGORY WHERE Category_Name=? AND User_Name=?", (categoryName, user_logged_in[0],)).fetchone()

    # If row does not exist, add the category. Otherwise alert the user.
    if row is None:
        cursor.execute("INSERT INTO CATEGORY VALUES (?, ?, ?)", (categoryName, user_logged_in[0], budget)) ## Tuple is needed for insert
        connection.commit()


        ### TODO: Probably need to add the html category here


        ###
        # connection.close()
    else:
        # Might need something else to handle this
        flash("Cannot have duplicate category names. Please pick another one.", "error")
        # time.sleep(5)

    connection.close()
    return redirect('/home')

if __name__ == '__main__':
    app.run(debug=True)