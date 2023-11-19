import os
import sqlite3
import unittest

import app

class TestAppEndpoints(unittest.TestCase):

    def setUp(self):

        app.DATABASE = './test_database.db'
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()

        # Connect to app.DATABASE
        connection = sqlite3.connect(app.DATABASE)
        cursor = connection.cursor()

        # Create tables in app.DATABASE
        cursor.execute("CREATE TABLE IF NOT EXISTS USER (User_Name TEXT PRIMARY KEY, Password TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS CATEGORY (Category_Name TEXT, User_Name TEXT, Budget_Amount TEXT, \
                            FOREIGN KEY (User_Name) REFERENCES USER (User_Name), \
                            PRIMARY KEY (Category_Name, User_Name))")
        cursor.execute("CREATE TABLE IF NOT EXISTS TRANSACTIONS (Transaction_ID TEXT, Category_Name TEXT, User_Name TEXT, \
                            Description TEXT, Money_Spent TEXT, Date TEXT, \
                            FOREIGN KEY (User_Name) REFERENCES USER (User_Name), \
                            FOREIGN KEY (Category_Name) REFERENCES CATEGORY (Category_Name), \
                            PRIMARY KEY (Transaction_ID, Category_Name, User_Name))")

        # Populate data for 1 user in app.DATABASE
        username = "DavidH"
        password = "password"

        cursor.execute("INSERT INTO USER VALUES (?, ?)", (username, password,))
        cursor.execute("INSERT INTO CATEGORY VALUES (?, ?, ?)", ('Default', username, 1000))
        cursor.execute("INSERT INTO TRANSACTIONS VALUES (?, ?, ?, ?, ?, ?)",
                        ('1', 'Default', 'DavidH', 'Water Bottle', '1.00', '2023-11-18 15:38:10.680185',))

        connection.commit()

        # Close connection to app.DATABASE
        connection.close()
    
    def tearDown(self):
        os.remove(app.DATABASE)

    def test_index(self):

        # Test GET request
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signup(self):

        # Test GET request
        response_get = self.client.get('/signup')
        self.assertEqual(response_get.status_code, 200)

        # Test valid POST request
        response_valid_post = self.client.post('/signup', data=dict(username='david', password='testing'), follow_redirects=True)
        self.assertEqual(response_valid_post.status_code, 200)

        # Test invalid POST request
        response_invalid_post = self.client.post('/signup', data=dict(username='DavidH', password='password'), follow_redirects=True)
        self.assertEqual(response_invalid_post.status_code, 200)

    def test_login(self):

        # Test GET request
        response_get = self.client.get('/login')
        self.assertEqual(response_get.status_code, 200)

        # Test valid POST request
        response_valid_post = self.client.post('/login', data=dict(username='DavidH', password='password'), follow_redirects=True)
        self.assertEqual(response_valid_post.status_code, 200)

        # Test invalid POST request
        response_invalid_post = self.client.post('/login', data=dict(username='DavidH', password='passwordfail'), follow_redirects=True)
        self.assertEqual(response_invalid_post.status_code, 200)

    def test_home(self):

        # Test invalid GET request
        response_invalid_get = self.client.get('/home')
        self.assertEqual(response_invalid_get.status_code, 401)

        # Login
        self.client.post('/login', data=dict(username='DavidH', password='password'))

        # Test valid GET request
        response_valid_get = self.client.get('/home')
        self.assertEqual(response_valid_get.status_code, 200)

    def test_logout(self):

        # Login
        self.client.post('/login', data=dict(username='DavidH', password='password'))

        # Test GET request
        response_get = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response_get.status_code, 200)

    def test_home_create_category(self):

        # Login
        self.client.post('/login', data=dict(username='DavidH', password='password'))

        # Connect to app.DATABASE
        connection = sqlite3.connect(app.DATABASE)
        cursor = connection.cursor()

        # Test valid POST
        self.client.post('/home/create-category', data={'category-name':'School', 'budget':'1000'})

        res_valid = cursor.execute("SELECT * FROM CATEGORY WHERE Category_Name=? AND User_Name=?", ("School", "DavidH",)).fetchone()
        self.assertEqual(res_valid, ("School", "DavidH", "1000.00"))

        # Test invalid POST
        self.client.post('/home/create-category', data={'category-name':'School', 'budget':'2000'})

        res_invalid = cursor.execute("SELECT * FROM CATEGORY WHERE Category_Name=? AND User_Name=?", ("School", "DavidH",)).fetchone()
        self.assertNotEqual(res_invalid, ("School", "DavidH", "2000.00"))

        # Close connection to app.DATABASE
        connection.close()

    def test_home_update_category(self):

        # Login
        self.client.post('/login', data=dict(username='DavidH', password='password'))

        # Connect to app.DATABASE
        connection = sqlite3.connect(app.DATABASE)
        cursor = connection.cursor()

        # Test valid POST
        self.client.post('/home/update-category', data={'old-category-name':'Default', 'new-category-name':'Misc', 'new-budget':'1500'})

        res_valid = cursor.execute("SELECT * FROM CATEGORY WHERE Category_Name=? AND User_Name=?", ("Misc", "DavidH",)).fetchone()
        self.assertEqual(res_valid, ("Misc", "DavidH", "1500.00"))

        # Test invalid POST
        self.client.post('/home/update-category', data={'old-category-name':'Food', 'new-category-name':'Foods', 'new-budget':'123abc'})

        res_valid = cursor.execute("SELECT * FROM CATEGORY WHERE Category_Name=? AND User_Name=?", ("Foods", "DavidH",)).fetchone()
        self.assertNotEqual(res_valid, ("Foods", "DavidH", "123abc.00"))

        # Close connection to app.DATABASE
        connection.close()

    def test_home_delete_category(self):

        # Login
        self.client.post('/login', data=dict(username='DavidH', password='password'))

        # Connect to app.DATABASE
        connection = sqlite3.connect(app.DATABASE)
        cursor = connection.cursor()

        # Test valid POST
        self.client.post('/home/delete-category', data={'category-name':'Default'})

        res_valid = cursor.execute("SELECT * FROM CATEGORY WHERE Category_Name=? AND User_Name=?", ("Default", "DavidH",)).fetchone()
        self.assertEqual(res_valid, None)

        res_valid = cursor.execute("SELECT * FROM TRANSACTIONS WHERE Category_Name=? AND User_Name=?", ("Default", "DavidH",)).fetchone()
        self.assertEqual(res_valid, None)

        # Close connection to app.DATABASE
        connection.close()

    def test_home_add_transaction(self):

        # Login
        self.client.post('/login', data=dict(username='DavidH', password='password'))

        # Connect to app.DATABASE
        connection = sqlite3.connect(app.DATABASE)
        cursor = connection.cursor()

        # Test valid POST
        self.client.post('/home/add-transaction', data={'category-name':'Default', 'transaction-description':'Lunch', 'money-spent':'6.55'})

        res_valid = cursor.execute("SELECT * FROM TRANSACTIONS WHERE Transaction_ID=? AND Category_Name=? AND User_Name=?",
                                    ("2", "Default", "DavidH",)).fetchone()
        res_tuple = (res_valid[0], res_valid[1], res_valid[2], res_valid[3], res_valid[4])
        self.assertEqual(res_tuple, ('2', 'Default', 'DavidH', 'Lunch', '6.55'))

        # Test invalid POST
        self.client.post('/home/add-transaction', data={'category-name':'Food', 'transaction-description':'Lunch', 'money-spent':'6.5usd'})

        res_valid = cursor.execute("SELECT * FROM TRANSACTIONS WHERE Transaction_ID=? AND Category_Name=? AND User_Name=?",
                                    ("3", "Default", "DavidH",)).fetchone()
        self.assertEqual(res_valid, None)

        # Close connection to app.DATABASE
        connection.close()

    def test_home_update_transaction(self):

        # Login
        self.client.post('/login', data=dict(username='DavidH', password='password'))

        # Connect to app.DATABASE
        connection = sqlite3.connect(app.DATABASE)
        cursor = connection.cursor()

        # Test valid POST
        self.client.post('/home/update-transaction', data={'category-name':'Default', 'old-transaction-id':'1',
                                                            'new-transaction-description':'Mineral Water', 'new-money-spent':'2.49'})

        res_valid = cursor.execute("SELECT * FROM TRANSACTIONS WHERE Transaction_ID=? AND Category_Name=? AND User_Name=?",
                                    ("1", "Default", "DavidH",)).fetchone()
        res_tuple = (res_valid[0], res_valid[1], res_valid[2], res_valid[3], res_valid[4])
        self.assertEqual(res_tuple, ('1', 'Default', 'DavidH', 'Mineral Water', '2.49'))

        # Test invalid POST
        self.client.post('/home/update-transaction', data={'category-name':'Default', 'old-transaction-id':'1',
                                                            'new-transaction-description':'Mineral Water', 'new-money-spent':'2.49abc'})

        res_valid = cursor.execute("SELECT * FROM TRANSACTIONS WHERE Transaction_ID=? AND Category_Name=? AND User_Name=?",
                                    ("1", "Default", "DavidH",)).fetchone()
        res_tuple = (res_valid[0], res_valid[1], res_valid[2], res_valid[3], res_valid[4])
        self.assertEqual(res_tuple, ('1', 'Default', 'DavidH', 'Mineral Water', '2.49'))

        # Close connection to app.DATABASE
        connection.close()

    def test_home_delete_transaction(self):

        # Login
        self.client.post('/login', data=dict(username='DavidH', password='password'))

        # Connect to app.DATABASE
        connection = sqlite3.connect(app.DATABASE)
        cursor = connection.cursor()

        # Test valid POST
        self.client.post('/home/delete-transaction', data={'category-name':'Default', 'transaction-id':'1'})

        res_valid = cursor.execute("SELECT * FROM TRANSACTIONS WHERE Transaction_ID=? AND Category_Name=? AND User_Name=?",
                                    ("1", "Default", "DavidH",)).fetchone()
        self.assertEqual(res_valid, None)

        # Close connection to app.DATABASE
        connection.close()

if __name__ == '__main__':
    unittest.main()