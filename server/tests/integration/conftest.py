import os
from datetime import datetime
from datetime import timedelta

import pytest
from app import create_app
from app.models.course_model import Course
from app.models.user_model import User
from flask_sqlalchemy import SQLAlchemy
from psycopg2.errors import DuplicateDatabase
from pytest_postgresql.factories import DatabaseJanitor

# DB_CONN = create_db_uri("test_bonniedotdev")
# DB_OPTS = sa.engine.url.make_url(DB_CONN).translate_connect_args()


# @pytest.fixture(scope="session")
# def database(request):
#     """
#     Create a Postgres database for the tests, and drop it when the tests are done.
#     """
#     pg_host = DB_OPTS.get("host")
#     pg_port = DB_OPTS.get("port")
#     pg_user = DB_OPTS.get("username")
#     pg_db = DB_OPTS["database"]

#     janitor = DatabaseJanitor(pg_user, pg_host, pg_port, pg_db, 9.6)
#     try:
#         janitor.init()
#     except DuplicateDatabase:
#         janitor.drop()
#         janitor.init()

#     @request.addfinalizer
#     def drop_database():
#         janitor.drop()


# @pytest.fixture(scope="session")
# def app(database):
#     """
#     Create a Flask app context for the tests.
#     """
#     app = Flask(__name__)

#     app.config["SQLALCHEMY_DATABASE_URI"] = DB_CONN

#     return app


# @pytest.fixture(scope="session")
# def _db(app):
#     """
#     Provide the transactional fixtures with access to the database via a
#     Flask-SQLAlchemy database connection.
#     """
#     db = SQLAlchemy(app=app)
#     db.init_app(app)

#     return db


@pytest.fixture(scope="session")
def database(request):
    user = os.getenv("PSQL_USERNAME")
    host = os.getenv("PSQL_HOST")
    port = os.getenv("PSQL_PORT")
    db_name = "test_bonniedotdev"
    janitor = DatabaseJanitor(user, host, port, db_name, 9.6)
    try:
        janitor.init()
    except DuplicateDatabase:
        janitor.drop()
        janitor.init()

    app = create_app(flask_env="test")
    db = SQLAlchemy()

    db.app = app
    db.init_app(app)

    yield db

    janitor.drop()


@pytest.fixture(scope="session")
def _db(database):
    return database


@pytest.fixture
def load_db_data(db_session):
    """Load test data into db."""

    future_iso_date = datetime.isoformat(datetime.now() + timedelta(days=30))
    past_iso_date = datetime.isoformat(datetime.now() - timedelta(days=30))

    courses = [
        {
            "name": "Awesome Course",
            "link": "https://udemy.com/awesomecourse",
            "description": "Whatta course!",
            "coupons": [
                {
                    "code": "NOT_EXPIRED",
                    "expiration_iso_string": future_iso_date,
                },
                {
                    "code": "EXPIRED",
                    "expiration_iso_string": past_iso_date,
                },
            ],
            "review_quotes": [
                {"review_quote": "the best!"},
                {"review_quote": "meh"},
            ],
        },
        {
            "name": "Simple Course",
            "link": "https://udemy.com/simplecourse",
            "description": "No coupons or reviews!",
        },
    ]
    users = [{"username": "admin", "password": "abc123"}]

    for course in courses:
        Course(**course)

    for user in users:
        User(**user)
