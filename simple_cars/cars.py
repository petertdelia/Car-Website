from flask import (
    Blueprint, render_template, request, flash, g
)

from simple_cars.db import get_db

bp = Blueprint('cars', __name__)

@bp.route('/cars', methods=('GET','POST'))
def index():
    page_number = int(request.args.get('page', '0'))

    db = get_db()
    cars = db.execute(
        'SELECT year,make,model,trim,drive,mileage,price FROM cars ORDER BY price'
    ).fetchall()

    if page_number == -1:
        page_number = len(cars) / 30

    cars = cars[30 * page_number : 30 * (page_number + 1)]

    return render_template('car_view/cars.html', cars=cars, page_number=page_number)

@bp.route('/cars/search', methods=('GET','POST'))
def search():
    if request.method =='POST':
        page_number = int(request.args.get('page', '0'))
        trim = request.form['trim']
        db = get_db()
        error = None

        if not trim:
            error = 'Trim is required.'

        if error is None:
            cars = db.execute(
                'SELECT * FROM cars WHERE trim = ? ORDER BY price', (trim,)
            ).fetchall()
            if page_number == -1:
                page_number = len(cars) / 30
            cars = cars[30 * page_number : 30 * (page_number + 1)]
            return render_template('car_view/cars.html', cars=cars, page_number=page_number)
        flash(error)

    db = get_db()
    trims = db.execute(
        'SELECT DISTINCT trim FROM cars'
    ).fetchall()

    return render_template('car_view/search.html', trims=trims)