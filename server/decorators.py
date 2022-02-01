from functools import wraps
from flask import request
from settings import TOKEN


def requires_auth(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not TOKEN:
            return function(*args, **kwargs)
        if not request.headers.get("Authorization", False):
            return {
                "success": False,
                "message": "Missing authentication header",
            }
        expected_token = f"Bearer {TOKEN}"
        if request.headers.get("Authorization") != expected_token:
            return {"success": False, "message": "Invalid token"}
        else:
            return function(*args, **kwargs)

    return decorated_function
