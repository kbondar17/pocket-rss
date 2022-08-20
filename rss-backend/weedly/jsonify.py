from typing import Any

import flask
import orjson


def jsonify(obj: Any) -> flask.Response:
    return flask.Response(
        orjson.dumps(obj),
        content_type='application/json',
    )
