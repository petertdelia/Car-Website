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
        page_number = len(cars) / 10

    cars = cars[10 * page_number : 10 * (page_number + 1)]

    return render_template('car_view/cars.html', cars=cars, page_number=page_number)

@bp.route('/cars/search', methods=('GET','POST'))
def search():
    
    db = get_db()
    trims = db.execute(
        'SELECT DISTINCT trim FROM cars'
    ).fetchall()
    drives = db.execute(
        'SELECT DISTINCT drive FROM cars'
    ).fetchall()

    return render_template('car_view/search.html', trims=trims, drives=drives)

@bp.route('/cars/search_results', methods=('GET','POST'))
def search_results():
    if request.method =='POST':
        db = get_db()
        key =  list(request.form)
        # meant to implement a function that checks that the key is valid
        # def switch_statement(key):
        #     switcher = {
        #         'trim',
        #         'drive'
        #     }
        #     if key in switcher:
        #         return True
        #     else:
        #         return False
        # valid = switch_statement(key)
        # if valid == True:
        value = request.form[key[0]]
        print(value)
        cars = db.execute(
            'SELECT * FROM cars WHERE ' + key[0] + ' = ? ORDER BY price', (value,)
        ).fetchall()
        # else:
        #     print('no valid key found!')
            
        page_number = int(request.args.get('page', '0'))
        
        cars = cars[10 * page_number : 10 * (page_number + 1)]
        if page_number == -1:
            page_number = len(cars) / 10
        cars = cars[10 * page_number : 10 * (page_number + 1)]

        return render_template('car_view/search_results.html', cars=cars, page_number=page_number, key=key[0], value=value)
    db = get_db()
    key =  request.args.get('key')
    value = request.args.get('value')
    page_number = int(request.args.get('page', '0'))
    cars = db.execute(
             'SELECT * FROM cars WHERE ' + key + ' = ? ORDER BY price', (value,)
         ).fetchall()
    if page_number == -1:
        page_number = len(cars) / 10
    cars = cars[10 * page_number : 10 * (page_number + 1)]
    
    return render_template('car_view/search_results.html', cars=cars, page_number=page_number, key=key, value=value)