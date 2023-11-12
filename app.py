from flask import Flask, render_template, request, redirect, abort, session, flash

import sqlite3
import uuid
import datetime

# Set up the database
DATABASE = './database.db'

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS USER (User_Name TEXT PRIMARY KEY, Password TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS CATEGORY (Category_Name TEXT, User_Name TEXT, Budget_Amount TEXT, FOREIGN KEY (User_Name) REFERENCES USER (User_Name), PRIMARY KEY (Category_Name, User_Name))")
cursor.execute("CREATE TABLE IF NOT EXISTS TRANSACTIONS (Transaction_ID TEXT, Category_Name TEXT, User_Name TEXT, Description TEXT, Money_Spent TEXT, Date TEXT, FOREIGN KEY (User_Name) REFERENCES USER (User_Name), FOREIGN KEY (Category_Name) REFERENCES CATEGORY (Category_Name), PRIMARY KEY (Transaction_ID, Category_Name, User_Name))")

connection.commit()

connection.close()

app = Flask('__name__')

app.config['SECRET_KEY'] = uuid.uuid4().hex

def get_category_data():

    category_data = dict()

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    category_rows = cursor.execute("SELECT * FROM CATEGORY WHERE User_Name=?", (session['username'],)).fetchall()

    for category_row in category_rows:
        transactions_for_category = dict()
        total_spent = 0.0

        transactions_rows = cursor.execute("SELECT * FROM TRANSACTIONS WHERE User_Name=? AND Category_Name=?", (session['username'],category_row[0],)).fetchall()
        for transactions_row in transactions_rows:
            transactions_for_category[f'{transactions_row[0]}'] = {'Description':f'{transactions_row[3]}',
                                                                    'Money_Spent':f'{transactions_row[4]}'}
            total_spent += float(transactions_row[4])
        
        transactions_for_category['Total_Spent'] = f'{total_spent:.2f}'
        transactions_for_category['Budget_Amount'] = f'{float(category_row[2]):.2f}'
            
        category_data[f'{category_row[0]}'] = transactions_for_category

    connection.close()

    return {'User_Name': f'{session["username"]}', 'Category_Data': category_data}

# An acceptable number is any non-negative value.
def is_acceptable_number(num):
    # Check if num is not an int or a float. Negative values get handled here.
    if num.isdigit() or num.replace(".", "", 1).isnumeric():
        return True
    return False

@app.route('/')
def index():

    # print(f'username/session: {session["username"]} {session["logged_in"]}')

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
            cursor.execute("INSERT INTO CATEGORY VALUES (?, ?, ?)", ('Default', username, 1000))
            connection.commit()
            connection.close()

            session['username'] = username
            session['logged_in'] = True

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
            connection.close()

            session['username'] = username
            session['logged_in'] = True

            print(f'username/session: {session["username"]} {session["logged_in"]}')

            return redirect('/home')

        else:
            connection.close()
            return render_template('login.html', title='Login', retry=True)

    return render_template('login.html', title='Login')  # This is a get, should there be an if statement?

@app.route('/home')
def home():
    # This should only be accessed by users who are logged in.
    if 'logged_in' in session and session['logged_in'] is True:
        user_expense_data = get_category_data()

        return render_template('home.html', title='Home', homepage="true", user_expense_data=user_expense_data)
    else:
        abort(403)

@app.route('/logout')
def logout():
    session['username'] = None
    session['logged_in'] = None

    print("in the logout endpoint")
    print(f'username/session: {session["username"]} {session["logged_in"]}')


    return redirect('/')

# Endpoint for creating a category.
@app.route('/home/create-category', methods=["POST"])
def createCategory():

    category_name = request.form.get('category-name')
    budget = request.form.get('budget')

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    row = cursor.execute("SELECT * FROM CATEGORY WHERE Category_Name=? AND User_Name=?", (category_name, session['username'],)).fetchone()

    # If row does not exist, add the category. Otherwise alert the user.  <--- this needs to be worked on
    # ^ could have an 'ERROR' var with the error msg, and pass to /home to display in html
    if row is None and is_acceptable_number(budget):
        cursor.execute("INSERT INTO CATEGORY VALUES (?, ?, ?)", (category_name, session['username'], f'{float(budget):.2f}')) ## Tuple is needed for insert
        
        connection.commit()
    else:
        print('ERROR in create-category: Category already exists')
        flash("Could not create category. Category already exists.")

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

    row = cursor.execute("SELECT * FROM CATEGORY WHERE Category_Name=? AND User_Name=?", (old_category_name, session['username'],)).fetchone()

    new_category_name_exists = cursor.execute("SELECT * FROM CATEGORY WHERE Category_Name=? AND User_Name=?", (new_category_name, session['username'],)).fetchone()

    print(f'new cat: {new_category_name_exists}')

    # User can keep the name of the same category.
    if new_category_name_exists is not None and new_category_name_exists[0] == old_category_name:
        new_category_name_exists = None

    # The row should exist if we want to update it.  <--- need to do something for the else
    if row is not None and new_category_name_exists is None and is_acceptable_number(new_budget):
        # Update the CATEGORY table
        cursor.execute("UPDATE CATEGORY SET Category_Name=?, Budget_Amount=? WHERE Category_Name=? AND User_Name=?", (new_category_name, f'{float(new_budget):.2f}', old_category_name, session['username'],))

        # Update the TRANSACTIONS table
        cursor.execute("UPDATE TRANSACTIONS SET Category_Name=? WHERE Category_Name=? AND User_Name=?", (new_category_name, old_category_name, session['username'],))

        connection.commit()
    else:
        print('ERROR in update-category: row does not exist, can\'t update!!!')
        flash("Could not update category. Old category either does not exist, new category already exists and/or new budget input is invalid.")

    connection.close()
    return redirect('/home')

# Endpoint for deleting a category.
@app.route('/home/delete-category', methods=["POST"])
def deleteCategory():

    category_name = request.form.get('category-name')
    
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    row = cursor.execute("SELECT * FROM CATEGORY WHERE Category_Name=? AND User_Name=?", (category_name, session['username'],)).fetchone()

    # The row should exist if we want to update it.  <--- need to do something for the else
    if row is not None:
        print("We're in the if condition")
        # Delete the specified category from the CATEGORY table
        cursor.execute("DELETE FROM CATEGORY WHERE Category_Name=? AND User_Name=?", (category_name, session['username'],))

        # Delete the transactions associated with the specified category from the TRANSACTIONS table
        cursor.execute("DELETE FROM TRANSACTIONS WHERE Category_Name=? AND User_Name=?", (category_name, session['username'],))

        connection.commit()
    else:
        print('ERROR in remove-category: row does not exist, can\'t remove!!!')
        flash("Could not delete category. Category does not exist.")

    connection.close()
    return redirect('/home')

# Endpoint for adding a transaction.
@app.route('/home/add-transaction', methods=["POST"])
def addTransaction():

    # TODO: how would I get the category name from the html?
    category_name = request.form.get('category-name')
    transaction_description = request.form.get('transaction-description')
    money_spent = request.form.get('money-spent')
    date = str(datetime.datetime.now())

    print('in add transaction')
    print(f'transaction: {transaction_description} -- spent: {money_spent}')
    print(category_name)

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    row = cursor.execute("SELECT * FROM CATEGORY WHERE Category_Name=? AND User_Name=?", (category_name, session['username'],)).fetchone()

    # Category needs to exist to add a transaction
    if row is not None and is_acceptable_number(money_spent):
        cursor.execute("INSERT INTO TRANSACTIONS VALUES (?, ?, ?, ?, ?, ?)", (None, category_name, session['username'], transaction_description, f'{float(money_spent):.2f}', date)) ## Tuple is needed for insert

        count = 0
        count = cursor.execute("SELECT COUNT(*) FROM TRANSACTIONS WHERE Category_Name=? AND User_Name=?", (category_name, session['username'],)).fetchone()

        if count:
            cursor.execute("UPDATE TRANSACTIONS SET Transaction_ID=? WHERE Category_Name=? AND User_Name=? AND Date=?", (count[0], category_name, session['username'], date))
        
        connection.commit()
    else:
        print(f'ERROR in create-category: No category name {category_name}')
        flash("Could not add transaction. Category does not exist and/or money spent input is invalid.")

    connection.close()

    return redirect('/home')

# Endpoint for updating a transaction.
@app.route('/home/update-transaction', methods=["POST"])
def updateTransaction():

    category_name = request.form.get('category-name')
    old_transaction_id = request.form.get('old-transaction-id')
    new_transaction_description = request.form.get('new-transaction-description')
    new_money_spent = request.form.get('new-money-spent')

    print(f'data: {category_name} , {old_transaction_id} , {new_transaction_description} , {new_money_spent}')

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    row = cursor.execute("SELECT * FROM TRANSACTIONS WHERE Transaction_ID=? AND Category_Name=? AND User_Name=?", (old_transaction_id, category_name, session['username'],)).fetchone()

    # The transaction must exist in order to update it.
    if row and is_acceptable_number(new_money_spent):
        cursor.execute("UPDATE TRANSACTIONS SET Description=?, Money_Spent=? WHERE Transaction_ID=? AND Category_Name=? AND User_Name=?", (new_transaction_description, f'{float(new_money_spent):.2f}', old_transaction_id, category_name, session['username']))

        connection.commit()
    
    else:
        print(f'ERROR in update-category: No transaction found with {old_transaction_id} , {category_name} and {session["username"]}')
        flash("Could not update transaction. Category does not exist, transaction id is invalid and/or new money spent input is invalid.")

    connection.close()

    return redirect('/home')

# Endpoint for deleting a transaction.
@app.route('/home/delete-transaction', methods=["POST"])
def deleteTransaction():
    print('in delete transaction')

    category_name = request.form.get('category-name')
    transaction_id = request.form.get('transaction-id')

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    row = cursor.execute("SELECT * FROM TRANSACTIONS WHERE Transaction_ID=? AND Category_Name=? AND User_Name=?", (transaction_id, category_name, session['username'],)).fetchone()

    # The transaction must exist in order to delete it.
    if row:
        cursor.execute("DELETE FROM TRANSACTIONS WHERE Transaction_ID=? AND Category_Name=? AND User_Name=?", (transaction_id, category_name, session['username']))

        transactions = cursor.execute("SELECT * FROM TRANSACTIONS WHERE Category_Name=? AND User_Name=? ORDER BY Date", (category_name, session['username'],)).fetchall()

        id_counter = 1
        for transaction in transactions:
            cursor.execute("UPDATE TRANSACTIONS SET Transaction_ID=? WHERE Transaction_ID=? AND Category_Name=? AND User_Name=?", (id_counter, transaction[0], category_name, session['username']))
            id_counter += 1

        connection.commit()
    else:
        print(f'ERROR in delete-category: No transaction found with {transaction_id} , {category_name} and {session["username"]}')
        flash("Could not delete transaction. Category does not exist and/or transaction id is invalid.")

    connection.close()

    return redirect('/home')


if __name__ == '__main__':
    app.run(debug=True)