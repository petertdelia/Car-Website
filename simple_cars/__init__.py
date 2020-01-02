from flask import (
    Flask, render_template, g, current_app, request, flash, redirect, url_for
)
import sqlite3, os
from simple_cars.db import get_db
from simple_cars.cars import is_car_in_collection, search

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='DEV',
        DATABASE=os.path.join(app.instance_path, 'cars_w_pics.sqlite')
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/')
    def index():
        return redirect(url_for('cars.search'))
    from . import cars, auth
    app.register_blueprint(cars.bp)
    app.register_blueprint(auth.bp)
    # app.add_url_rule('/cars/search', endpoint='search')
    app.jinja_env.globals.update(is_car_in_collection=is_car_in_collection)

    return app
    

    


