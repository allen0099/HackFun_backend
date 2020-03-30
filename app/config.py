import configparser


class Config:
    JSON_SORT_KEYS: bool = False

    SECRET_KEY: str = None

    SQL_ADMIN: str = "root"
    SQL_PASSWORD: str = "meowmeow"
    SQL_LOC: str = "127.0.0.1"
    SQL_PORT: str = "32769"
    SQL_SCHEMA: str = "testing"

    SQLALCHEMY_DATABASE_URI: str = f"mysql://{SQL_ADMIN}:{SQL_PASSWORD}@{SQL_LOC}:{SQL_PORT}/{SQL_SCHEMA}"

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False


class DevConfig(Config):
    SECRET_KEY: str = "dev"

    SQL_ADMIN: str = "root"
    SQL_PASSWORD: str = "meowmeow"
    SQL_LOC: str = "127.0.0.1"
    SQL_PORT: str = "32769"
    SQL_SCHEMA: str = "develop"
    SQLALCHEMY_DATABASE_URI: str = f"mysql://{SQL_ADMIN}:{SQL_PASSWORD}@{SQL_LOC}:{SQL_PORT}/{SQL_SCHEMA}"


class ProductionConfig(Config):
    config = configparser.ConfigParser()
    config.read("credentials/flask.ini")
    SECRET_KEY = config['Flask']['secretKey']

    SQL_SCHEMA: str = "develop"


config: dict = {
    "config": Config,
    "development": DevConfig,

    "production": ProductionConfig
}
