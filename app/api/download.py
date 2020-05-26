from typing import List

from flask import Response, send_from_directory, abort
from flask_login import login_required

from app.api import api
from app.models import Docker


@api.route('/download/<string:filename>')
@login_required
def download(filename: str) -> Response:
    hash_binary_list: List[str] = Docker.get_binary_list()
    if filename in hash_binary_list:
        return send_from_directory("static", filename, as_attachment=True)
    return abort(404)
