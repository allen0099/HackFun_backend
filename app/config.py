import configparser


class Config:
    JSON_SORT_KEYS: bool = False

    SECRET_KEY: str = None

    SQL_ADMIN: str = ""
    SQL_PASSWORD: str = ""
    SQL_LOC: str = ""
    SQL_PORT: str = ""
    SQL_SCHEMA: str = ""

    SQLALCHEMY_DATABASE_URI: str = f"mysql://{SQL_ADMIN}:{SQL_PASSWORD}@{SQL_LOC}:{SQL_PORT}/{SQL_SCHEMA}"

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False


class DevConfig(Config):
    SECRET_KEY: str = "dev"

    SQL_ADMIN: str = "root"
    # SESSION_PROTECTION = "strong"
    SQL_PASSWORD: str = "meowmeow"
    SQL_LOC: str = "127.0.0.1"
    SQL_PORT: str = "32769"
    SQL_SCHEMA: str = "develop"
    SQLALCHEMY_DATABASE_URI: str = f"mysql://{SQL_ADMIN}:{SQL_PASSWORD}@{SQL_LOC}:{SQL_PORT}/{SQL_SCHEMA}"


class ProductionConfig(Config):
    config: configparser = configparser.ConfigParser()
    config.read("credentials/flask.ini")

    SECRET_KEY = config['Flask']['secretKey']

    sql_config: configparser = configparser.ConfigParser()
    sql_config.read("credentials/flask.ini")

    sql: dict = sql_config["sql"]

    SQL_ADMIN: str = sql.get("admin")
    SQL_PASSWORD: str = sql.get("password")
    SQL_LOC: str = sql.get("loc")
    SQL_PORT: str = sql.get("port")
    SQL_SCHEMA: str = sql.get("schema")
    SQLALCHEMY_DATABASE_URI: str = f"mysql://{SQL_ADMIN}:{SQL_PASSWORD}@{SQL_LOC}:{SQL_PORT}/{SQL_SCHEMA}"


config: dict = {
    "config": Config,
    "development": DevConfig,

    "production": ProductionConfig
}
