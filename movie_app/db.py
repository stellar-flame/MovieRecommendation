import sqlite3
import click
import csv
import os

from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    populate(db,
             os.path.join(os.path.dirname(__file__), '../data', 'ratings.csv'),
             'INSERT INTO rating (userId, movieId, rating, timestamp) VALUES (?, ?, ?, ?)')

    populate(db,
             os.path.join(os.path.dirname(__file__), '../data', 'movies.csv'),
             'INSERT INTO movie (movieId, title, genres) VALUES (?, ?, ?)')

    print('Database populated')

def populate(db, csv_file_path, sql_string):
    # Open the CSV file
    with open(csv_file_path, 'r') as file:
        # Use csv.reader to read the file
        csv_reader = csv.reader(file)

        # Skip the header row (if present)
        next(csv_reader, None)

        # Insert the CSV data into the ratings table
        db.executemany(sql_string, csv_reader)

    # Commit the changes and close the connection
    db.commit()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)