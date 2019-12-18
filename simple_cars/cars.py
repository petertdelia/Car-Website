from flask import (
    Blueprint, render_template, request, flash, g, redirect, url_for
)
from simple_cars.db import get_db

bp = Blueprint('cars', __name__)

def build_sql_statement(sortBy,**kwargs):
    db = get_db()
    return_dict = {}
    cars_query = 'SELECT * FROM cars'
    cars_query_params = []
    i = 0
    for key,value in kwargs.items():
        db_query = 'SELECT DISTINCT ' + key + ' FROM cars'
        if value and i == 0:
            cars_query += " WHERE {0} =?".format(key)
            cars_query_params.append(value)
            i += 1
        elif value:
            cars_query += " AND {0} =?".format(key)
            cars_query_params.append(value)
        query_params = []
        temp_key = key
        j=0
        for key1,value1 in kwargs.items():
            if value1 and key1 != temp_key:
                if j == 0:
                    db_query += " WHERE {0} =?".format(key1)
                    query_params.append(value1)
                    j+=1
                else:
                    db_query += " AND {0} =?".format(key1)
                    query_params.append(value1)
        search_result = db.execute(db_query,query_params).fetchall()
        return_dict.update({key + 's' : search_result})
    cars_query += " ORDER BY {0}".format(sortBy)
    car_search_result = db.execute(cars_query, cars_query_params).fetchall()
    return_dict.update({'cars' : car_search_result})
    return return_dict

def get_car_info(year,trim,drive,sortBy):
    db = get_db()

    if not year and not trim and not drive:
        years = db.execute(
            'SELECT DISTINCT year FROM cars'
        ).fetchall()
        trims = db.execute(
            'SELECT DISTINCT trim FROM cars'
        ).fetchall()
        drives = db.execute(
            'SELECT DISTINCT drive FROM cars'
        ).fetchall()
        cars = db.execute(
            'SELECT * FROM cars ORDER BY ' + sortBy
        ).fetchall()
        return years, trims, drives, cars
    elif not trim and not drive:
        years = db.execute(
            'SELECT DISTINCT year FROM cars'
        ).fetchall()
        trims = db.execute(
            'SELECT DISTINCT trim FROM cars WHERE year=?', (year,)
        ).fetchall()
        drives = db.execute(
            'SELECT DISTINCT drive FROM cars WHERE year=?', (year,)
        ).fetchall()
        cars = db.execute(
            'SELECT * FROM cars WHERE year=? ORDER BY ' + sortBy, 
            (year,)
        ).fetchall()
        return years, trims, drives, cars
    elif not year and not drive:
        years = db.execute(
            'SELECT DISTINCT year FROM cars WHERE trim=?', (trim,)
        ).fetchall()
        trims = db.execute(
            'SELECT DISTINCT trim FROM cars'
        ).fetchall()
        drives = db.execute(
            'SELECT DISTINCT drive FROM cars WHERE trim=?', (trim,)
        ).fetchall()
        cars = db.execute(
            'SELECT * FROM cars WHERE trim=? ORDER BY ' + sortBy, 
            (trim,)
        ).fetchall()
        return years, trims, drives, cars
    elif not year and not trim:
        years = db.execute(
            'SELECT DISTINCT year FROM cars WHERE drive=?', (drive,)
        ).fetchall()
        trims = db.execute(
            'SELECT DISTINCT trim FROM cars WHERE drive=?', (drive,)
        ).fetchall()
        drives = db.execute(
            'SELECT DISTINCT drive FROM cars'
        ).fetchall()
        cars = db.execute(
            'SELECT * FROM cars WHERE drive=? ORDER BY ' + sortBy, 
            (drive,)
        ).fetchall()
        return years, trims, drives, cars         
    elif not year:
        years = db.execute(
            'SELECT DISTINCT year FROM cars WHERE drive=? AND trim=?', (drive, trim)
        ).fetchall()
        trims = db.execute(
            'SELECT DISTINCT trim FROM cars WHERE drive=?', (drive,)
        ).fetchall()
        drives = db.execute(
            'SELECT DISTINCT drive FROM cars WHERE trim=?', (trim,)
        ).fetchall()
        cars = db.execute(
            'SELECT * FROM cars WHERE drive=? AND trim=? ORDER BY ' + sortBy, 
            (drive, trim)
        ).fetchall()
        return years, trims, drives, cars
    elif not trim:
        years = db.execute(
            'SELECT DISTINCT year FROM cars WHERE drive=?', (drive,)
        ).fetchall()
        trims = db.execute(
            'SELECT DISTINCT trim FROM cars WHERE drive=? AND year=?', (drive, year)
        ).fetchall()
        drives = db.execute(
            'SELECT DISTINCT drive FROM cars'
        ).fetchall()
        cars = db.execute(
            'SELECT * FROM cars WHERE drive=? AND year=? ORDER BY ' + sortBy, 
            (drive, year)
        ).fetchall()
        return years, trims, drives, cars 
    elif not drive:
        years = db.execute(
            'SELECT DISTINCT year FROM cars WHERE trim=?', (trim,)
        ).fetchall()
        trims = db.execute(
            'SELECT DISTINCT trim FROM cars WHERE year=?', (year,)
        ).fetchall()
        drives = db.execute(
            'SELECT DISTINCT drive FROM cars WHERE year=? AND trim=?', (year, trim)
        ).fetchall()        
        cars = db.execute(
            'SELECT * FROM cars WHERE year=? AND trim=? ORDER BY ' + sortBy, 
            (year, trim)
        ).fetchall()    
        return years, trims, drives, cars             
    else:
        years = db.execute(
            'SELECT DISTINCT year FROM cars WHERE drive= ? AND trim=?', (drive, trim)
        ).fetchall()
        trims = db.execute(
            'SELECT DISTINCT trim FROM cars WHERE drive=? AND year=?', (drive, year)
        ).fetchall()
        drives = db.execute(
            'SELECT DISTINCT drive FROM cars WHERE trim=? AND year=?', (trim, year)
        ).fetchall()
        cars = db.execute(
            'SELECT * FROM cars WHERE year=? AND trim=? AND drive=? ORDER BY ' + sortBy, 
            (year, trim, drive)
        ).fetchall()            
        return years, trims, drives, cars             

# is there a js way to generalize the sort list on the html? this function seems inefficient: 
def get_column_names(table_name):
    db = get_db()
    names = db.execute('pragma table_info(' + table_name + ')').fetchall()
    column_names = []
    i = 0
    for name in names:
        column_names.append(name[1])
        i += 1
    return column_names

@bp.route('/')
def go_to():
    return redirect(url_for('cars.search'))

@bp.route('/cars', methods=('GET','POST'))
def index():
    db = get_db()
    page_number = int(request.args.get('page', '0'))
    column_names = get_column_names('cars')
    sortBy = request.args.get('sortBy', 'price')

    cars = db.execute(
        'SELECT * FROM cars ORDER BY ' + sortBy
    ).fetchall()

    if page_number == -1:
        page_number = len(cars) // 10
    total_pages = len(cars) // 10

    cars = cars[10 * page_number : 10 * (page_number + 1)]

    return render_template('car_view/index.html', cars=cars, page_number=page_number, 
        total_pages=total_pages, sortBy=sortBy, column_names=column_names)

@bp.route('/cars/search', methods=('GET','POST'))
def search():
    
    column_names = get_column_names('cars')
    if request.args.get('year', '') != '':
        year = int(request.args.get('year', ''))
    else:
        year = ''

    trim = request.args.get('trim', '') 
    drive = request.args.get('drive', '')
    sortBy = request.args.get('sortBy', 'price')
    page_number = int(request.args.get('page', '0'))

    kwargs = build_sql_statement(sortBy,trim=trim,drive=drive,year=year)

    # years, trims, drives, cars = get_car_info(year,trim,drive,sortBy)

    total_pages = len(kwargs['cars']) // 10
    if page_number > total_pages:
        page_number = total_pages
    if page_number == -1:
            page_number = len(kwargs['cars']) // 10
    kwargs['cars'] = kwargs['cars'][10 * page_number : 10 * (page_number + 1)]

    return render_template('car_view/search.html', **kwargs, 
        year=year, trim=trim, drive=drive, page_number=page_number, sortBy=sortBy,
        total_pages=total_pages, column_names=column_names)

@bp.route('/cars/search_results', methods=('GET','POST'))
def search_results():
    column_names = get_column_names('cars')
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
    year = request.args.get('year', '')
    trim = request.args.get('trim', '') 
    drive = request.args.get('drive', '')

    db = get_db()
    column_names = get_column_names('cars')
    car = db.execute(
        'SELECT * FROM cars WHERE ID = ?', (car_id,)
    ).fetchone()

    return render_template('car_view/single_car.html', 
        year=year, trim=trim, drive=drive, car=car, 
        column_names=column_names, sortBy = sortBy, page_number = page_number)

