import configparser


class Config:
    JSON_SORT_KEYS: bool = False

    SECRET_KEY: str = None

    SQLALCHEMY_DATABASE_URI: str = None
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    @staticmethod
    def init_app(app):
        pass


class TestConfig(Config):
    SECRET_KEY: str = "testingString"
    SQLALCHEMY_DATABASE_URI: str = "mysql://root:meowmeow@127.0.0.1:32769/testing"


class DevelopmentConfig(Config):
    SECRET_KEY: str = b'(ML\x90\x13\xcd\xaev\xa0 \x1d\x1fC\xab\xb7\x05'
    SQLALCHEMY_DATABASE_URI: str = "mysql://root:meowmeow@127.0.0.1:32769/develop"


class ProductionConfig(Config):
    config = configparser.ConfigParser()
    config.read("credentials.ini")
    SECRET_KEY = config['Flask']['secretKey']
    SQLALCHEMY_DATABASE_URI: str = "mysql://root:meowmeow@127.0.0.1:32769/production"


config = {
    "test": TestConfig,
    "develop": DevelopmentConfig,
    "product": ProductionConfig,

    "default": DevelopmentConfig
}
