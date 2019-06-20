from flask import (
    Flask, render_template, g
)
import sqlite3
app = Flask(__name__)

def get_db():
    g.db = sqlite3.connect(
        'cars.sqlite',
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    g.db.row_factory = sqlite3.Row
    return g.db


@app.route('/cars')
def display_cars_db():
    db = get_db()
    cars = db.execute(
        'SELECT year,make,model,trim,mileage FROM cars'
    ).fetchall()
    db.close()
    return render_template('car_view/cars.html', cars=cars)
    


