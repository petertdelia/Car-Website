from flask import Flask
import sqlite3
app = Flask(__name__)


@app.route('/cars')
def display_cars_db():
    db = sqlite3.connect('cars.sqlite')
    cars = db.execute(
        'SELECT * FROM cars'
    ).fetchall()
    return str(cars + "hi mom!")
    


