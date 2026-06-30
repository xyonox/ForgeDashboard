from sql import *
from nicegui import app, ui

def get_users_exercises(username: str):
    try:
        user_obj = User.get(User.username == username)
        exercises = Exercise.select().where(Exercise.user == user_obj)
        formatted_exercises = [{"name": exercise.name, "description": exercise.description} for exercise in exercises]
        return formatted_exercises
    except Exception as e:
        print(f"Benutzer nicht gefunden: {e}")
        return [] # Leere Liste zurückgeben, wenn der User nicht existiert

def get_users_exercises_names(username: str):
    try:
        user_obj = User.get(User.username == username)
        exercises = Exercise.select().where(Exercise.user == user_obj)
        formatted_exercises = [exercise.name for exercise in exercises]
        return formatted_exercises
    except Exception as e:
        print(f"Benutzer nicht gefunden: {e}")
        return [] # Leere Liste zurückgeben, wenn der User nicht existiert

def create_or_update_exercise_weekday(
        username: str,
        exercise_name: str,
        weekday_id: int,
        sets: str,
        workout_position: int = None):

    user_obj = User.get(User.username == username)
    weekday_obj = Weekday.get_by_id(weekday_id)
    exercise_obj = Exercise.get(Exercise.name == exercise_name)

    if workout_position is None:
        max_position = (
            ExerciseWeekday
            .select(fn.MAX(ExerciseWeekday.workout_position))
            .where(

                ExerciseWeekday.user == user_obj,

                ExerciseWeekday.weekday == weekday_obj

            )
            .scalar()
        )

        workout_position = 1 if max_position is None else max_position + 1

    obj, created = ExerciseWeekday.get_or_create(
        user=user_obj,
        weekday=weekday_obj,
        exercise=exercise_obj,
        defaults={
            "workout_position": workout_position,
            "sets": sets
        }
    )

    if not created:
        obj.sets = sets
        obj.save()

def track_exercise(username, exercise_name, sets, weights):
    try:
        ExerciseTrack.create(user=User.get(User.username == username), exercise=Exercise.get(Exercise.name == exercise_name), track_sets=sets, track_weights=weights)
        return True
    except Exception as e:
        print(f"Error tracking exercise: {e}")
        return False

def move_exercise(username: str, weekday_id: int, exercise_name: str, new_position: int):

    user = User.get(User.username == username)

    weekday = Weekday.get_by_id(weekday_id)
    exercise = Exercise.get(Exercise.name == exercise_name)

    obj = ExerciseWeekday.get(
        ExerciseWeekday.user == user,
        ExerciseWeekday.weekday == weekday,
        ExerciseWeekday.exercise == exercise
    )

    old_position = obj.workout_position
    max_position = (

        ExerciseWeekday
        .select(fn.COUNT(ExerciseWeekday.id))
        .where(
            ExerciseWeekday.user == user,
            ExerciseWeekday.weekday == weekday
        )
        .scalar()
    )

    new_position = max(1, min(new_position, max_position))

    if new_position == old_position:
        return

    with get_db().atomic():
        obj.workout_position = -1

        obj.save()

        if new_position < old_position:
            (
                ExerciseWeekday.update(

                    workout_position=ExerciseWeekday.workout_position + 1

                )
                .where(
                    ExerciseWeekday.user == user,
                    ExerciseWeekday.weekday == weekday,
                    ExerciseWeekday.workout_position >= new_position,
                    ExerciseWeekday.workout_position < old_position
                )
                .execute()
            )

        else:

            (

                ExerciseWeekday.update(

                    workout_position=ExerciseWeekday.workout_position - 1

                )

                .where(

                    ExerciseWeekday.user == user,

                    ExerciseWeekday.weekday == weekday,

                    ExerciseWeekday.workout_position <= new_position,

                    ExerciseWeekday.workout_position > old_position

                )

                .execute()

            )

        obj.workout_position = new_position

        obj.save()

def delete_exercise_weekday(username: str, exercise_name: str, weekday_id: int):
    ExerciseWeekday.delete().where(
        ExerciseWeekday.user == User.get(User.username == username),
        ExerciseWeekday.exercise == Exercise.get(Exercise.name == exercise_name),
        ExerciseWeekday.weekday_id == weekday_id
    ).execute()


def create_exercise(username: str, name: str, description: str):
    try:
        Exercise.create(
            user=User.get(User.username == username),
            name=name,
            description=description
        )
    except Exception as e:
        print(f"Exercise already exists or error: {e}")


def update_exercise(username: str, exercise_id: int, name: str, description: str):
    try:
        Exercise.update(
            name=name,
            description=description
        ).where(Exercise.id == exercise_id).execute()
    except Exception as e:
        print(f"Exercise not found or update failed: {e}")


def delete_exercise(exercise_name: str):
    try:
        Exercise.delete().where(Exercise.name == exercise_name).execute()
    except Exception as e:
        print(f"Exercise not found or delete failed: {e}")


def get_workout_plan(username: str):
    try:
        user_obj = User.get(User.username == username)

        query = (ExerciseWeekday
                 .select(ExerciseWeekday, Exercise, Weekday)
                 .join(Exercise)
                 .switch(ExerciseWeekday)
                 .join(Weekday)
                 .where(ExerciseWeekday.user == user_obj)
                 .order_by(Weekday.day_index, ExerciseWeekday.workout_position))

        days_names = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        workout_plan = {day: [] for day in days_names.values()}

        for plan in query:
            current_day_name = days_names[plan.weekday.day_index]
            exercise_info = {
                "position": plan.workout_position,
                "name": plan.exercise.name,
                "description": plan.exercise.description,
                "sets": plan.sets
            }
            workout_plan[current_day_name].append(exercise_info)

        return workout_plan
    except Exception as e:
        print(f"Error getting workout plan: {e}")
        return None