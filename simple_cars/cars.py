from flask import (
    Blueprint, render_template, request, flash, g
)
from simple_cars.db import get_db

bp = Blueprint('cars', __name__)

def get_car_info():
    db = get_db()

    models = db.execute(
        'SELECT DISTINCT model FROM cars'
    ).fetchall()
    trims = db.execute(
        'SELECT DISTINCT trim FROM cars'
    ).fetchall()
    drives = db.execute(
        'SELECT DISTINCT drive FROM cars'
    ).fetchall()
    return models, trims, drives



@bp.route('/cars', methods=('GET','POST'))
def index():
    page_number = int(request.args.get('page', '0'))

    db = get_db()
    sortBy = request.args.get('sortBy', 'price')
    if request.method == "POST":
        sortBy = request.args.get('sortBy', 'price')
    cars = db.execute(
        'SELECT year,make,model,trim,drive,mileage,price FROM cars ORDER BY ' + sortBy
    ).fetchall()

    if page_number == -1:
        page_number = len(cars) / 10
    total_pages = len(cars) / 10

    cars = cars[10 * page_number : 10 * (page_number + 1)]

    return render_template('car_view/index.html', cars=cars, page_number=page_number, total_pages=total_pages, sortBy=sortBy)

@bp.route('/cars/search', methods=('GET','POST'))
def search():
    
    models, trims, drives = get_car_info()
    return render_template('car_view/search.html', trims=trims, drives=drives, models=models)

@bp.route('/cars/search_results', methods=('GET','POST'))
def search_results():
    if request.method =='POST':
        db = get_db()
        temp_key =  list(request.form)
        key = temp_key[0]
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
        value = request.form[key]
        print(key) 
        print(value)
        cars = db.execute(
            'SELECT * FROM cars WHERE ' + key + ' = ? ORDER BY price', (value,)
        ).fetchall()
        # else:
        #     print('no valid key found!')
            
        page_number = int(request.args.get('page', '0'))
        total_pages = len(cars) / 10
        
        if page_number == -1:
            page_number = len(cars) / 10
    
        cars = cars[10 * page_number : 10 * (page_number + 1)]

        return render_template('car_view/search_results.html', cars=cars, page_number=page_number, total_pages=total_pages, key=key, value=value)
    db = get_db()
    key =  request.args.get('key')
    value = request.args.get('value')
    page_number = int(request.args.get('page', '0'))
    cars = db.execute(
             'SELECT * FROM cars WHERE ' + key + ' = ? ORDER BY price', (value,)
         ).fetchall()
    if page_number == -1:
        page_number = len(cars) / 10
    total_pages = len(cars) / 10
    cars = cars[10 * page_number : 10 * (page_number + 1)]
    
    return render_template('car_view/search_results.html', cars=cars, page_number=page_number, total_pages=total_pages, key=key, value=value)

@bp.route('/cars/text_search_results', methods=('GET','POST'))
def text_search_results():

    car = list(request.form)
    value = request.form[car[0]]
    print(car)
    print(value)
    # the following function checks if the search value is in the database, identifies it, then returns the correct query from the db.
    def sorter(value):
        models, trims, drives = get_car_info()



    return render_template('car_view/text_search_results.html', value=value)



@bp.route('/cars/individual_view')
def view():

    # trying to get the car row id to come through to uniquely identify the car and then return its info from the db
    car_id = request.args.get('car_id', 'error')
    db = get_db()
    car = db.execute(
        'SELECT * FROM cars WHERE ID = ?', (car_id,)
    ).fetchone()

    return render_template('car_view/single_car.html', car=car)

