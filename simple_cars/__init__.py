from flask import (
    Flask, render_template, g, current_app, request, flash
)
import sqlite3, os
from simple_cars.db import get_db

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='DEV',
        DATABASE=os.path.join(app.instance_path, 'cars.sqlite')
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import cars
    app.register_blueprint(cars.bp)
    app.add_url_rule('/cars', endpoint='index')

    return app
    

    


