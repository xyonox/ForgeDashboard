from nicegui import ui,app
import ui_elements as eui
import services.user_service as us
import services.workout_service as ws

@ui.refreshable
def add_workout_exercise():
    pass

@ui.page("/workout_tracker")
def mainpage():
    if not us.is_logged_in():
        return

    days = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }

    user = us.get_user()

    exercises = ws.get_users_exercises_names(user.username)

    def add_exercise_to_user():
        if exercise_name_input.value == "":
            ui.notify("Please enter an exercise name")
            return
        if exercise_name_input.value in exercises:
            ui.notify("Exercise already exists")
            return
        ws.create_exercise(user.username, exercise_name_input.value, exercise_description_input.value)
        add_workout_exercise.refresh()
        exercises.append(exercise_name_input.value)
        exercise_name_input.value=""
        exercise_description_input.value=""


    eui.header()
    with ui.row().classes("gap-4"):
        with ui.card().classes("w-screen"):
            workout_day_select = ui.select(
                options=days,
                with_input=True,
                label="Select Day",
                on_change=lambda e: ui.notify(f"Selected Day-ID: {e.value} ({days[e.value]})")
            ).classes("w-64 text-black")

            workout_day_select.props('popup-content-class="text-black bg-white"')


    with ui.row().classes("gap-4"):
        with ui.card().classes("m-full"):
            ui.label("Workout Tracker")
            exercise_name_input = ui.input("Exercise Name")
            exercise_description_input = ui.input("Exercise Name")
            ui.button("Add Exercise", on_click=add_exercise_to_user)

        with ui.card().classes("m-full"):
            exercise_select = ui.select(
                options=exercises,
                with_input=True,
                label="Select Exercise",
                on_change=lambda e: ui.notify(f"Selected: {e.value}")
            ).classes("w-64 text-black")

            exercise_select.props('popup-content-class="text-black bg-white"')

            add_workout_exercise()

            day_select = ui.select(
                options=days,
                with_input=True,
                label="Select Day",
                on_change=lambda e: ui.notify(f"Selected Day-ID: {e.value} ({days[e.value]})")
            ).classes("w-64 text-black")

            day_select.props('popup-content-class="text-black bg-white"')

            sets_input = ui.input(placeholder="e.g. 3x15")
