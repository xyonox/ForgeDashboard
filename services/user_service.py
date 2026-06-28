import sql
from sql import *
from nicegui import app, ui
from argon2 import PasswordHasher, exceptions as argon2_exceptions

pwHasher = PasswordHasher()

def is_logged_in():
    try:
        if not app.storage.user["is_auth"]:
            ui.navigate.to("/login")
            return False
    except:
        ui.navigate.to("/login")
        return False
    return True

def cookie_login(username):
    app.storage.user["username"] = username
    app.storage.user["is_auth"] = True

def logout():
    app.storage.user["username"] = None
    app.storage.user["is_auth"] = False

def login(username, password):
    user = User.get_or_none(username=username)
    if user is None:
        return False
    try:
        pwHasher.verify(user.password_hash, password)
    except argon2_exceptions.VerificationError:
        return False
    cookie_login(username)
    ui.navigate.to("/")
    return True

def register(username, password):
    if len(password) > 8:
        ui.notify("Das Passwort muss mindestens 8 Zeichen lang sein")
        return False
    pw_hash = pwHasher.hash(password)
    try:
        User.create(username=username, password_hash=pw_hash)
    except peewee.IntegrityError:
        ui.notify("Der Username ist bereits vergeben")
        return False
    cookie_login(username)
    return login(username, password)