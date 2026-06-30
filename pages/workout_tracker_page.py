from nicegui import ui,app
import ui_elements as eui
import services.user_service as us
import services.workout_service as ws

days = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }

@ui.refreshable
def workout_plan_scroll_area(workout_day_select):

    user = us.get_user()
    workout_plan = ws.get_workout_plan(user.username)

    with ui.scroll_area().classes("h-160 w-screen"):

        def track_progress(exercise_name, sets, weights):
            success = ws.track_exercise(user.username, exercise_name, sets, weights)
            if success:
                ui.notify("Exercise tracked successfully!")
            else:
                ui.notify("Failed to track exercise.")

        @ui.refreshable
        def build_area():
            ui.label("Workout Plan").classes("text-xl")

            selected_day = days[workout_day_select.value]
            ui.label(f"Day: {selected_day}")

            exercises = workout_plan[selected_day]

            if not exercises:
                ui.label("No exercises planned.")
                return

            def draw_exercise_card(exercise):
                with eui.card().classes("w-52 h-117"):
                    ui.label(exercise["name"]).classes("text-lg font-bold")
                    ui.label(f'Sets: {exercise["sets"]}')

                    ui.label("Progress").classes("text-lg font-bold")

                    ui.label("Reps")
                    reps_input = ui.input(placeholder="e.g. 15 13 12").classes("w-full")

                    ui.label("Weight")
                    weights_input = ui.input(placeholder="e.g. 2x7kg 6kg").classes("w-full")

                    eui.button(
                        "Add Progress",
                        on_click=lambda: track_progress(exercise["name"], reps_input.value, weights_input.value)
                    )

                    with ui.row().classes("justify-between w-full mt-4"):
                        eui.button(
                            "⬆",
                            on_click=lambda: (
                                ws.move_exercise(
                                    user.username,
                                    workout_day_select.value + 1,
                                    exercise["name"],
                                    max(1, exercise["position"] - 1),
                                ),
                                workout_plan_scroll_area.refresh(),
                            ),
                        )

                        eui.button(
                            "⬇",
                            on_click=lambda: (
                                ws.move_exercise(
                                    user.username,
                                    workout_day_select.value + 1,
                                    exercise["name"],
                                    exercise["position"] + 1,
                                ),
                                workout_plan_scroll_area.refresh(),
                            ),
                        )

            with ui.grid(columns=6).classes("w-full gap-3"):
                for exercise in exercises:
                    with ui.row().classes("justify-between w-full"):
                        draw_exercise_card(exercise)

        build_area()

    workout_day_select.on(
        "update:model-value",
        lambda _: build_area.refresh()
    )


@ui.page("/workout_tracker")
def mainpage():
    if not us.is_logged_in():
        return

    user = us.get_user()

    exercises = ws.get_users_exercises_names(user.username)


    eui.header()
    with ui.row().classes("gap-4"):
        with eui.card().classes("w-screen h-170"):
            workout_day_select = eui.select(
                options=days,
                value=0,
                label="Select Day",
            )
            workout_plan_scroll_area(workout_day_select)

    reveal_edit_area_button = eui.button("edit workout plan").classes("m-2")

    def build_edit_workout_plan_area():
        reveal_edit_area_button.delete()
        with eui.card():
            def add_exercise_to_user():
                if exercise_name_input.value == "":
                    ui.notify("Please enter an exercise name")
                    return
                if exercise_name_input.value in exercises:
                    ui.notify("Exercise already exists")
                    return
                ws.create_exercise(user.username, exercise_name_input.value, exercise_description_input.value)
                exercises.append(exercise_name_input.value)
                exercise_name_input.value = ""
                exercise_description_input.value = ""

            with ui.row().classes("gap-4"):
                with eui.card().classes("m-full") as edit_area:
                    ui.label("Workout Tracker")
                    exercise_name_input = ui.input("Exercise Name")
                    exercise_description_input = ui.input("Description")
                    eui.button("Add Exercise", on_click=add_exercise_to_user)

                def add_exercise_to_workout():
                    if not exercise_select.value:
                        ui.notify("Please select an exercise")
                        return

                    if day_select.value is None:
                        ui.notify("Please select a day")
                        return

                    if not sets_input.value:
                        ui.notify("Please enter sets")
                        return

                    ws.create_or_update_exercise_weekday(
                        user.username,
                        exercise_select.value,
                        day_select.value+1,
                        sets_input.value,
                    )

                    ui.notify("Workout added!")
                    workout_plan_scroll_area.refresh()

                with eui.card().classes("m-full") as add_workout_area:
                    exercise_select = eui.select(
                        options=exercises,
                        with_input=True,
                        label="Select Exercise",
                        on_change=lambda e: ui.notify(f"Selected: {e.value}")
                    )


                    day_select = eui.select(
                        options=days,
                        with_input=True,
                        label="Select Day",
                        on_change=lambda e: ui.notify(f"Selected Day-ID: {e.value} ({days[e.value]})")
                    )

                    sets_input = ui.input(placeholder="e.g. 3x15")

                    eui.button("Add Workout", on_click=lambda: add_exercise_to_workout())

    reveal_edit_area_button.on_click(build_edit_workout_plan_area)