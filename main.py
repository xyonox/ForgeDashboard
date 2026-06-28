import secrets

from nicegui import *
from sql import *
import pages.main_page as mainpage
import pages.login_register_pages
import pages.workout_tracker_page

init_db()

ui.run(storage_secret=secrets.token_urlsafe(32))