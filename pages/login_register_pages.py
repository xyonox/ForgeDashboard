import ui_elements as eui
from nicegui import ui
import services.user_service as us

@ui.page("/login")
def login_page():
    def login_submit():
        un = username_input.value
        pw = password_input.value
        us.login(un, pw)

    eui.header()
    with ui.card().classes("m-full"):
        username_input = ui.input(placeholder="Username")
        password_input = ui.input(password=True, placeholder="Password")

        ui.button("Login", on_click=login_submit)
        ui.link("Register", "/register")

@ui.page("/register")
def register_page():
    def register_submit():
        un = username_input.value
        pw = password_input.value
        us.register(un, pw)

    eui.header()
    with ui.card().classes("m-full"):
        username_input = ui.input(placeholder="Username")
        password_input = ui.input(password=True, placeholder="Password")

        ui.button("Register", on_click=register_submit)
        ui.link("Login", "/login")
