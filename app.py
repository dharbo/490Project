from flask import Flask, render_template, request, redirect, abort, flash

import sqlite3
import uuid

# Set up the database
DATABASE = './database.db'

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS USER (User_Name TEXT PRIMARY KEY, Password TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS CATEGORY (Category_Name TEXT, User_Name TEXT, Budget_Amount TEXT, FOREIGN KEY (User_Name) REFERENCES USER (User_Name), PRIMARY KEY (Category_Name, User_Name))")
cursor.execute("CREATE TABLE IF NOT EXISTS TRANSACTIONS (Transaction_ID TEXT, Category_Name TEXT, User_Name TEXT, Description TEXT, Money_Spent TEXT, FOREIGN KEY (User_Name) REFERENCES USER (User_Name), FOREIGN KEY (Category_Name) REFERENCES CATEGORY (Category_Name), PRIMARY KEY (Transaction_ID, Category_Name, User_Name))")

## TESTING with transactions
# cursor.execute("INSERT OR IGNORE INTO TRANSACTIONS VALUES (?,?,?,?,?)", ('4','Insurance','david','Farmers','100'))
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
        total_spent = 0.0

        transactions_rows = cursor.execute("SELECT * FROM TRANSACTIONS WHERE User_Name=? AND Category_Name=?", (user_logged_in[0],category_row[0],)).fetchall()
        for transactions_row in transactions_rows:
            transactions_for_category[f'{transactions_row[0]}'] = {'Description':f'{transactions_row[3]}',
                                                                    'Money_Spent':f'{transactions_row[4]}'}
            total_spent += float(transactions_row[4])
        
        transactions_for_category['Total_Spent'] = f'{total_spent}'
        transactions_for_category['Budget_Amount'] = f'{float(category_row[2])}'
            
        category_data[f'{category_row[0]}'] = transactions_for_category

    connection.close()

    return {'User_Name': f'{user_logged_in[0]}', 'Category_Data': category_data}

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
        user_expense_data = get_category_data()

        return render_template('home.html', title='Home', homepage="true", user_expense_data=user_expense_data)
    else:
        abort(403)

# Endpoint for creating a category.
@app.route('/home/create-category', methods=["POST"])
def createCategory():

    category_name = request.form.get('category-name')
    budget = request.form.get('budget')

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    row = cursor.execute("SELECT * FROM CATEGORY WHERE Category_Name=? AND User_Name=?", (category_name, user_logged_in[0],)).fetchone()

    # If row does not exist, add the category. Otherwise alert the user.  <--- this needs to be worked on
    # ^ could have an 'ERROR' var with the error msg, and pass to /home to display in html
    if row is None:
        cursor.execute("INSERT INTO CATEGORY VALUES (?, ?, ?)", (category_name, user_logged_in[0], budget)) ## Tuple is needed for insert
        
        connection.commit()
    else:
        print('ERROR in create-category: Category already exists')

    connection.close()
    return redirect('/home')

# Endpoint for updating a category.
@app.route('/home/update-category', methods=["POST"])
def updateCategory(): ### TODO: just changed the category table, need to also change all rows in the transaction table with old cat-name to new cat-name

    old_category_name = request.form.get('old-category-name')
    new_category_name = request.form.get('new-category-name')
    new_budget = request.form.get('new-budget')

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    row = cursor.execute("SELECT * FROM CATEGORY WHERE Category_Name=? AND User_Name=?", (old_category_name, user_logged_in[0],)).fetchone()

    # The row should exist if we want to update it.  <--- need to do something for the else
    if row is not None:
        # Update the CATEGORY table
        cursor.execute("UPDATE CATEGORY SET Category_Name=?, Budget_Amount=? WHERE Category_Name=? AND User_Name=?", (new_category_name, new_budget, old_category_name, user_logged_in[0],))

        # Update the TRANSACTIONS table
        cursor.execute("UPDATE TRANSACTIONS SET Category_Name=? WHERE Category_Name=? AND User_Name=?", (new_category_name, old_category_name, user_logged_in[0],))

        connection.commit()
    else:
        print('ERROR in update-category: row does not exist, can\'t update!!!')

    connection.close()
    return redirect('/home')

# Endpoint for deleting a category.
@app.route('/home/delete-category', methods=["POST"])
def deleteCategory():

    category_name = request.form.get('category-name')
    
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    row = cursor.execute("SELECT * FROM CATEGORY WHERE Category_Name=? AND User_Name=?", (category_name, user_logged_in[0],)).fetchone()

    # The row should exist if we want to update it.  <--- need to do something for the else
    if row is not None:
        print("We're in the if condition")
        # Delete the specified category from the CATEGORY table
        cursor.execute("DELETE FROM CATEGORY WHERE Category_Name=? AND User_Name=?", (category_name, user_logged_in[0],))

        # Delete the transactions associated with the specified category from the TRANSACTIONS table
        cursor.execute("DELETE FROM TRANSACTIONS WHERE Category_Name=? AND User_Name=?", (category_name, user_logged_in[0],))

        connection.commit()
    else:
        print('ERROR in remove-category: row does not exist, can\'t remove!!!')

    connection.close()
    return redirect('/home')

if __name__ == '__main__':
    app.run(debug=True)