import hashlib
import os
from typing import List

from flask import Flask


class BinaryChecker():
    def __init__(self, app: Flask = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        with app.app_context():
            # rename file with its sha256
            file_list: List[str] = os.listdir(app.static_folder)
            _original: str = os.getcwd()
            os.chdir(app.static_folder)
            for file in file_list:
                with open(file, "rb")as f:
                    # noinspection InsecureHash
                    sha256sum = hashlib.sha256(f.read()).hexdigest()
                    if file != sha256sum:
                        os.rename(file, sha256sum)

            from app.models import Docker
            from app import db

            # https://stackoverflow.com/a/49178408
            if Docker.__tablename__ in db.inspect(db.engine).get_table_names():
                file_list: List[str] = os.listdir(app.static_folder)
                hash_list: List[str] = Docker.get_binary_list()
                if set(hash_list) != set(file_list):
                    raise FileNotFoundError

            os.chdir(_original)
