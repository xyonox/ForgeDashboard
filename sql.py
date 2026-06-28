import peewee
from peewee import *

def get_db():
    return SqliteDatabase('forge.db')

class CodingSession(Model):

    daytime = DateField(unique=True)
    minutes = IntegerField()

    class Meta:
        database = get_db()

class TestUser(Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = get_db()

class User(Model):
    username = CharField(unique=True)
    password_hash = CharField()

    class Meta:
        database = get_db()

def init_db():
    print("Initializing database")
    db = get_db()
    db.connect()
    print("Creating tables")

    try:
        db.create_tables([CodingSession, TestUser, User])
        print("Tables created")
    except:
        print("Tables already exist")
    print("Creating test variables")
    # Bei create wird es versucht immer wieder neu zu erstellen, bei get_or_create nur wenn es nicht existiert
    TestUser.get_or_create(username="test", password="Nutte")

