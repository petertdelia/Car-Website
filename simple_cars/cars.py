from flask import (
    Blueprint, render_template, request, flash, g
)

from simple_cars.db import get_db

bp = Blueprint('cars', __name__)

@bp.route('/cars', methods=('GET','POST'))
def index():

    db = get_db()
    cars = db.execute(
        'SELECT year,make,model,trim,mileage FROM cars'
    ).fetchall()

    return render_template('car_view/cars.html', cars=cars)

@bp.route('/cars/search', methods=('GET','POST'))
def search():
    if request.method =='POST':
        
        trim = request.form['trim']
        db = get_db()
        error = None

        if not trim:
            error = 'Trim is required.'

        if error is None:
            cars = db.execute(
                'SELECT * FROM cars WHERE trim = ?', (trim,)
            )
            return render_template('car_view/cars.html', cars=cars)
        flash(error)

    db = get_db()
    trims = db.execute(
        'SELECT DISTINCT trim FROM cars'
    ).fetchall()

    return render_template('car_view/search.html', trims=trims)