from datetime import datetime
from datetime import timedelta

import pytest
import sqlalchemy as sa
from app.models.course_model import Course
from app.models.user_model import User
from config import create_db_uri
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pytest_postgresql.factories import drop_postgresql_database
from pytest_postgresql.factories import init_postgresql_database

DB_CONN = create_db_uri("test_bonniedotdev")
DB_OPTS = sa.engine.url.make_url(DB_CONN).translate_connect_args()


@pytest.fixture(scope="session")
def database(request):
    """
    Create a Postgres database for the tests, and drop it when the tests are done.
    """
    pg_host = DB_OPTS.get("host")
    pg_port = DB_OPTS.get("port")
    pg_user = DB_OPTS.get("username")
    pg_db = DB_OPTS["database"]

    init_postgresql_database(pg_user, pg_host, pg_port, pg_db)

    @request.addfinalizer
    def drop_database():
        drop_postgresql_database(pg_user, pg_host, pg_port, pg_db, 9.6)


@pytest.fixture(scope="session")
def app(database):
    """
    Create a Flask app context for the tests.
    """
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = DB_CONN

    return app


@pytest.fixture(scope="session")
def _db(app):
    """
    Provide the transactional fixtures with access to the database via a
    Flask-SQLAlchemy database connection.
    """
    db = SQLAlchemy(app=app)

    return db


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
