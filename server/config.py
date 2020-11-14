"""Flask settings for this app."""
import os


def create_db_uri(db_name):
    """Create db URI from env vars and db name."""

    user = os.getenv("PSQL_USERNAME")
    pw = os.getenv("PSQL_PASSWORD")
    host = os.getenv("PSQL_HOST")
    port = os.getenv("PSQL_PORT")

    return f"postgresql://{user}:{pw}@{host}:{port}/{db_name}"


class CommonConfig:
    """Common settings."""

    # process and return all reqparse errors, rather than stopping at the first
    BUNDLE_ERRORS = True

    # keep app secure
    SECRET_KEY = os.getenv("FLASK_SECRET")

    # don't need to keep track of DB changes
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(CommonConfig):
    """Settings for production."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = create_db_uri("bonniedotdev")


class DevConfig(CommonConfig):
    """Settings for development."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = create_db_uri("dev_bonniedotdev")


class TestConfig(CommonConfig):
    """Settings for test."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = create_db_uri("test_bonniedotdev")


# to make it easier to select which config to use without conditionals
app_config = {
    "production": ProductionConfig,
    "development": DevConfig,
    "test": TestConfig,
}
