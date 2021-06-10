from functools import wraps

from flask import jsonify

from api.core.exceptions import ValidationError, EntityDoesNotExist


def error_handler(fn):
    @wraps(fn)
    def wrapped_fn(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except ValidationError as ex:
            return jsonify({'errors': ex.errors}), 400
        except EntityDoesNotExist as ex:
            return jsonify({'errors': ex.errors}), 404
    return wrapped_fn
