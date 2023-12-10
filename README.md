# Capstone Project
Software for capstone project (CPSC 490/491)

## Summary
The idea is to create an application where users can visually see their monthly expenses. Users would be able to manually input their transactions to track any purchases they make and categorize these transactions so that they can see what types of things they are spending their money on.

## Prerequisites
Flask, Tailwind CSS, Node.js, and npm are needed for this application.

To install Flask, run:

`pip install Flask`

To install Node.js and npm, run:

`sudo apt install nodejs`

`sudo apt install npm`

To install Tailwind CSS, run:

`npm install -D tailwindcss`

## Usage
To run the application locally, enter this in the terminal: `npm run dev`

This will host the application on http://127.0.0.1:5000.

## Run Unit Tests
In order to run the unit tests for this project, simply run the `unit_tests.py` script.

To run this script, run:

`python3 unit_tests.py`

If successful, an "OK" message will be returned.

## Primary Features
Users can create an account or login if they already have one. After that, users will be directed to their home page which is where their transactions are displayed. Once here, users can create new categories, update existing categories, and delete existing categories. Users can also add transactions to specific categories, update transactions, and delete transactions. The information entered will remain the same unless changed, meaning that if they logout and then log back, their categories and transactions will still be there.
