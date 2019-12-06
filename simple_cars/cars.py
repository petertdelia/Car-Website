from flask import (
    Blueprint, render_template, request, flash, g, redirect, url_for
)
from simple_cars.db import get_db

bp = Blueprint('cars', __name__)

def get_car_info(model,trim,drive):
    db = get_db()

    if not model and not trim and not drive:
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
    elif not trim and not drive:
        models = db.execute(
            'SELECT DISTINCT model FROM cars'
        ).fetchall()
        trims = db.execute(
            'SELECT DISTINCT trim FROM cars WHERE model=?', (model,)
        ).fetchall()
        drives = db.execute(
            'SELECT DISTINCT drive FROM cars WHERE model=?', (model,)
        ).fetchall()
        return models, trims, drives
    elif not model and not drive:
        models = db.execute(
            'SELECT DISTINCT model FROM cars WHERE trim=?', (trim,)
        ).fetchall()
        trims = db.execute(
            'SELECT DISTINCT trim FROM cars'
        ).fetchall()
        drives = db.execute(
            'SELECT DISTINCT drive FROM cars WHERE trim=?', (trim,)
        ).fetchall()
        return models, trims, drives  
    elif not model and not trim:
        models = db.execute(
            'SELECT DISTINCT model FROM cars WHERE drive=?', (drive,)
        ).fetchall()
        trims = db.execute(
            'SELECT DISTINCT trim FROM cars WHERE drive=?', (drive,)
        ).fetchall()
        drives = db.execute(
            'SELECT DISTINCT drive FROM cars'
        ).fetchall()
        return models, trims, drives         
    elif not model:
        models = db.execute(
            'SELECT DISTINCT model FROM cars WHERE drive=? AND trim=?', (drive, trim)
        ).fetchall()
        trims = db.execute(
            'SELECT DISTINCT trim FROM cars WHERE drive=?', (drive,)
        ).fetchall()
        drives = db.execute(
            'SELECT DISTINCT drive FROM cars WHERE trim=?', (trim,)
        ).fetchall()
        return models, trims, drives  
    elif not trim:
        models = db.execute(
            'SELECT DISTINCT model FROM cars WHERE drive=?', (drive,)
        ).fetchall()
        trims = db.execute(
            'SELECT DISTINCT trim FROM cars WHERE drive=? AND model=?', (drive, model)
        ).fetchall()
        drives = db.execute(
            'SELECT DISTINCT drive FROM cars'
        ).fetchall()
        return models, trims, drives 
    elif not drive:
        models = db.execute(
            'SELECT DISTINCT model FROM cars WHERE trim=?', (trim,)
        ).fetchall()
        trims = db.execute(
            'SELECT DISTINCT trim FROM cars WHERE model=?', (model,)
        ).fetchall()
        drives = db.execute(
            'SELECT DISTINCT drive FROM cars WHERE model=? AND trim=?', (model, trim)
        ).fetchall()            
        return models, trims, drives             
    else:
        models = db.execute(
            'SELECT DISTINCT model FROM cars WHERE drive= ? AND trim=?', (drive, trim)
        ).fetchall()
        trims = db.execute(
            'SELECT DISTINCT trim FROM cars WHERE drive=? AND model=?', (drive, model)
        ).fetchall()
        drives = db.execute(
            'SELECT DISTINCT drive FROM cars WHERE trim=? AND model=?', (trim, model)
        ).fetchall()            
        return models, trims, drives             

# is there a js way to generalize the sort list on the html? this function seems inefficient: 
def get_column_names():
    db = get_db()
    names = db.execute('pragma table_info(cars)').fetchall()
    column_names = []
    i = 0
    for name in names:
        column_names.append(name[1])
        i += 1
    return column_names

@bp.route('/')
def go_to():
    return redirect(url_for('cars.index'))

@bp.route('/cars', methods=('GET','POST'))
def index():
    db = get_db()
    page_number = int(request.args.get('page', '0'))
    column_names = get_column_names()
    sortBy = request.args.get('sortBy', 'price')

    cars = db.execute(
        'SELECT ID,year,make,model,trim,drive,mileage,price FROM cars ORDER BY ' + sortBy
    ).fetchall()

    if page_number == -1:
        page_number = len(cars) // 10
    total_pages = len(cars) // 10

    cars = cars[10 * page_number : 10 * (page_number + 1)]

    return render_template('car_view/index.html', cars=cars, page_number=page_number, 
        total_pages=total_pages, sortBy=sortBy, column_names=column_names)

@bp.route('/cars/search', methods=('GET','POST'))
def search():
    
    column_names = get_column_names()
    model = request.args.get('model', '')
    trim = request.args.get('trim', '') 
    drive = request.args.get('drive', '')
    sortBy = request.args.get('sortBy', 'price')
    page_number = int(request.args.get('page', '0'))
    models, trims, drives = get_car_info(model,trim,drive)

    db = get_db()
    cars = db.execute(
            'SELECT * FROM cars WHERE model = ? AND trim = ? and drive = ? ORDER BY ' + sortBy, 
            (model,trim,drive)
        ).fetchall()
    cars = cars[10 * page_number : 10 * (page_number + 1)]
    page_number = int(request.args.get('page', '0'))
    total_pages = len(cars) // 10

    return render_template('car_view/search.html', trims=trims, drives=drives, models=models, 
        model=model, trim=trim, drive=drive, cars=cars, page_number=page_number, sortBy=sortBy,
        total_pages=total_pages, column_names=column_names)

@bp.route('/cars/search_results', methods=('GET','POST'))
def search_results():
    column_names = get_column_names()
    if request.method =='POST':
        db = get_db()
        print(len(list(request.args)))
        # this if else statement is not good...it's messing up my sorting. Need to be able to parse the dict that comes through
        if len(list(request.args)) == 1:
            temp_key =  list(request.args)
            key = temp_key[0]
            value = request.args[key]
        else:
            key =  request.args.get('key')
            value = request.args.get('value')
        print("args: " + str(request.args))
        print("form: " + str(request.form))
         

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
        # else:
        #     print('no valid key found!')
        
        sortBy = request.args.get('sortBy', 'price')
        print("key: " + key)
        print("value: " + value)
        cars = db.execute(
            'SELECT * FROM cars WHERE ' + key + ' = ? ORDER BY ' + sortBy, (value,)
        ).fetchall()


        page_number = int(request.args.get('page', '0'))
        total_pages = len(cars) // 10
        
        if page_number == -1:
            page_number = len(cars) // 10
    
        cars = cars[10 * page_number : 10 * (page_number + 1)]

        return render_template('car_view/search_results.html', column_names = column_names, cars=cars, page_number=page_number, 
            total_pages=total_pages, key=key, value=value, sortBy=sortBy)
    db = get_db()
    key =  request.args.get('key')
    value = request.args.get('value')
    sortBy = request.args.get('sortBy', 'price')
    page_number = int(request.args.get('page', '0'))
    cars = db.execute(
             'SELECT * FROM cars WHERE ' + key + ' = ? ORDER BY ' + sortBy, (value,)
         ).fetchall()
    if page_number == -1:
        page_number = len(cars) // 10
    total_pages = len(cars) // 10
    cars = cars[10 * page_number : 10 * (page_number + 1)]
    
    return render_template('car_view/search_results.html', column_names = column_names, cars=cars, 
        page_number=page_number, total_pages=total_pages, key=key, value=value, sortBy=sortBy)

@bp.route('/cars/text_search_results', methods=('GET','POST'))
def text_search_results():

    car = list(request.form)
    value = request.form[car[0]]
    # the following function checks if the search value is in the database, identifies it, then returns the correct query from the db.
    def sorter(value):
        models, trims, drives = get_car_info()

    return render_template('car_view/text_search_results.html', value=value)

@bp.route('/cars/individual_view')
def view():

    # trying to get the car row id to come through to uniquely identify the car and then return its info from the db
    car_id = request.args.get('car_id', 'error')
    sortBy = request.args.get('sortBy', 'price')
    page_number = request.args.get('page', '0')
    key = request.args.get('key', 'ford')
    value = request.args.get('value', 'edge')

    db = get_db()
    column_names = get_column_names()
    car = db.execute(
        'SELECT * FROM cars WHERE ID = ?', (car_id,)
    ).fetchone()

    return render_template('car_view/single_car.html', key=key, value=value, car=car, column_names=column_names, sortBy = sortBy, page_number = page_number)

