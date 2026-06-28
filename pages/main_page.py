from nicegui import ui,app
import ui_elements as eui
import services.user_service as us

@ui.page("/")
def mainpage():
    us.is_logged_in()

    eui.header()
    ui.label("Hello " + app.storage.user["username"])
    print("Hello World")