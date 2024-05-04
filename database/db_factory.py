from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_db(app):
    """
    Configures and returns a database instance bound to a Flask application.

    :param app: Flask application instance
    :return: Configured database instance
    """
    db.init_app(app)
    return db
