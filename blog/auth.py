from functools import wraps
from flask import request, Response, session
from blog import config
from blog import db

from argon2 import PasswordHasher

def check_auth(username, password):
    """ This function is called to check if a username / password
        combination is valid.
    """
    cur = db.connection.cursor()
    ph = PasswordHasher()
    try:
        cur.execute(f"SELECT * FROM users WHERE email='{username}'")
        user = cur.fetchone()
        if user is None or not ph.verify(user.get("password"), password):
            return False
    except Exception:
        return False
    user = cur.fetchone()

    if user is None:
        return False

    session["is_logged_in"] = True
    session["id"] = user.get("id")
    session["email"] = user.get("email")
    session["full_name"] = user.get("full_name")

    return True

    # return username == config.username and password == config.password


def authenticate():
    """ Sends a 401 response that enables basic auth. """
    return Response('Not authorized to access this URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return func(*args, **kwargs)
    return decorated
