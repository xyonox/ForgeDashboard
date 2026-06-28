import peewee
from peewee import *

def get_db():
    return SqliteDatabase('forge.db')

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

class Exercise(Model):
    user = ForeignKeyField(User, backref='exercises')
    name = CharField(unique=True)
    description = TextField()
    class Meta: database = get_db()

class Weekday(Model):
    # Speichert 0 = Montag, 1 = Dienstag etc.
    day_index = IntegerField(unique=True)
    class Meta: database = get_db()

# DIE ZWISCHENTABELLE
class ExerciseWeekday(Model):
    user = ForeignKeyField(User, backref='workout_plans')
    exercise = ForeignKeyField(Exercise, backref='days')
    weekday = ForeignKeyField(Weekday, backref='exercises')

    workout_position = IntegerField()
    sets = TextField()

    class Meta:
        database = get_db()
        # verhindert, dass gleiche workout_position gleichzeitig existieren
        indexes = (
            (('user' ,'weekday', 'workout_position'), True),
        )



def init_db():
    print("Initializing database")
    db = get_db()
    db.connect()
    print("Creating tables")

    try:
        tables_to_create = [
            TestUser,
            User,
            Exercise,
            Weekday,
            ExerciseWeekday
        ]
        db.create_tables(tables_to_create, safe=True)
        print("Tables created")

        for i in range(7):
            Weekday.get_or_create(day_index=i)
        print("Weekdays initialized (0-6)")
    except:
        print("something went wrong:")
        print(db.get_tables())
    print("Creating test variables")
    # Bei create wird es versucht immer wieder neu zu erstellen, bei get_or_create nur wenn es nicht existiert
    TestUser.get_or_create(username="test", password="Sollte zensiert werden")

