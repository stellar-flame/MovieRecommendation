import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://movierecuser:yourpassword@localhost/movierecommendations',
    #     SQLALCHEMY_TRACK_MODIFICATIONS=False
    # )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .database import db_session

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    from . import auth
    app.register_blueprint(auth.bp)

    from . import movies
    app.register_blueprint(movies.bp)
    app.add_url_rule('/', endpoint='index')

    return app
