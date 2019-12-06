from flask import (
    g, current_app
)
import sqlite3

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
        g.db.row_factory = sqlite3.Row

    return g.db

def get_relevant_car_info(**kwargs):
	db = get_db()
	for key, value in kwargs.items():
		print("%s == %s" %(key, value))