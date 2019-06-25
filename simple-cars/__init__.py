from flask import (
    Flask, render_template, g, current_app
)
import sqlite3, os

app = Flask(__name__)
app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'cars.sqlite')
)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
                current_app.config['DATABASE'],
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
    return render_template('car_view/cars.html', cars=cars)
    


