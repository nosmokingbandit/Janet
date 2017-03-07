from lib import htmlPy
from backend import BackEnd
from backend import Options
from backend import Library
from backend import Gui
import os
import imp
import sys
from core import log
import core
from PySide import QtGui


def get_base_dir():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    else:
        return os.path.abspath(os.path.dirname(__file__))


BASE_DIR = get_base_dir()


if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.abspath(os.path.dirname(__file__))

os.chdir(application_path)


app = htmlPy.AppGUI(title=u"Janet", developer_mode=True)
app.maximized = False
app.web_app.setMinimumWidth(940)
app.web_app.setMinimumHeight(768)
app.window.setWindowIcon(QtGui.QIcon(BASE_DIR + "/static/images/janet.png"))
#app.right_click_setting(htmlPy.settings.INPUTS_ONLY)
app.static_path = os.path.join(BASE_DIR, "static/")
app.template_path = os.path.join(BASE_DIR, "templates/")

if __name__ == "__main__":
    app.bind(BackEnd(app))

    options = Options(app)
    app.bind(options)
    library = Library(app)
    app.bind(library)
    gui = Gui(app)
    app.bind(gui)

    if core.CONFIG.get('start_maximized') == "true":
        app.maximized = True
    if core.CONFIG.get('start_fullscreen') == "true":
        app.window.showFullScreen()

    app.template = ("index.html", {"cwd": os.getcwd(),
                                   "scan_on_load": core.CONFIG.get('scan_on_load'),
                                   "start_fullscreen": core.CONFIG.get('start_fullscreen')
                                   })

    app.start()
