import wx
from cefpython3 import cefpython as cef
import platform
import sys
import os
import core
from core import jshandler, options

print os.getcwd()

# Get base dir for when running with pyinstaller
core.BASE_DIR = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.abspath(os.path.dirname(__file__))

# Fix for PyCharm hints warnings when using static methods
WindowUtils = cef.WindowUtils()

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Configuration
WIDTH = 960
HEIGHT = 540

# Globals
g_count_windows = 0


def check_versions():
    print("[wxpython.py] CEF Python {ver}".format(ver=cef.__version__))
    print("[wxpython.py] Python {ver} {arch}".format(
            ver=platform.python_version(), arch=platform.architecture()[0]))
    print("[wxpython.py] wxPython {ver}".format(ver=wx.version()))
    # CEF Python version requirement
    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"


class MainFrame(wx.Frame):
    ''' Creates Window '''

    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY,
                          title='Janet', size=(WIDTH, HEIGHT))
        self.SetMinSize((WIDTH, HEIGHT))

        self.browser = None

        global g_count_windows
        g_count_windows += 1

        self.setup_icon()
        # self.create_menu()
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Set wx.WANTS_CHARS style for the keyboard to work.
        # This style also needs to be set for all parent controls.
        self.browser_panel = wx.Panel(self, style=wx.WANTS_CHARS)
        self.browser_panel.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.browser_panel.Bind(wx.EVT_SIZE, self.OnSize)

        # On Linux must show before embedding browser, so that handle
        # is available.
        if LINUX:
            self.Show()
            self.embed_browser()
        else:
            self.embed_browser()
            self.Show()

        wx.CallLater(500, self.setup_gamepad)  # this has to be delayed to make sure the DOM has loaded the list of games

    def setup_gamepad(self):
        self.gamepad_connected = False
        self.stick = wx.Joystick()
        self.stick.SetCapture(self)
        self.gamepad_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.poll_gamepad, self.gamepad_timer)
        self.gamepad_timer.Start(150)  # 150ms seems to be a good rate, we aren't playing Street Fighter or anything.

    def poll_gamepad(self, event):
        if not self.FindFocus():
            return
        if not self.gamepad_connected and self.stick.IsOk():
            self.gamepad_connected = True
            self.browser.ExecuteFunction('gamepad_status', True)
        elif self.gamepad_connected and not self.stick.IsOk():
            self.gamepad_connected = False
            self.browser.ExecuteFunction('gamepad_status', False)
            return
        if self.gamepad_connected is False:
            return

        commands = {}
        dpad_pos = {65535: None, 18000: 'down', 0: 'up', 27000: 'left', 9000: 'right'}.get(self.stick.GetPOVPosition())
        if dpad_pos:
            commands['dpad'] = dpad_pos

        buttons = self.stick.GetButtonState()
        if buttons:
            commands['buttons'] = buttons

        if commands != {}:
            self.browser.ExecuteFunction('gamepad_input', commands)

    def setup_icon(self):
        icon_file = os.path.join(core.BASE_DIR, 'janet.png')
        if os.path.exists(icon_file):
            icon = wx.IconFromBitmap(wx.Bitmap(icon_file, wx.BITMAP_TYPE_PNG))
            self.SetIcon(icon)

    def create_menu(self):
        filemenu = wx.Menu()
        filemenu.Append(1, "Some option")
        filemenu.Append(2, "Another option")
        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        self.SetMenuBar(menubar)

    def embed_browser(self):
        window_info = cef.WindowInfo()
        (width, height) = self.browser_panel.GetClientSizeTuple()
        window_info.SetAsChild(self.browser_panel.GetHandle(),
                               [0, 0, width, height])

        index = os.path.join(core.BASE_DIR, 'templates', 'loader.html')
        self.browser = cef.CreateBrowserSync(window_info, url=index)
        self.browser.SetClientHandler(FocusHandler())

    def OnSetFocus(self, _):
        if not self.browser:
            return
        if WINDOWS:
            WindowUtils.OnSetFocus(self.browser_panel.GetHandle(),
                                   0, 0, 0)
        self.browser.SetFocus(True)

    def OnSize(self, _):
        if not self.browser:
            return
        if WINDOWS:
            WindowUtils.OnSize(self.browser_panel.GetHandle(),
                               0, 0, 0)
        elif LINUX:
            (x, y) = (0, 0)
            (width, height) = self.browser_panel.GetSizeTuple()
            self.browser.SetBounds(x, y, width, height)
        self.browser.NotifyMoveOrResizeStarted()

    def OnClose(self, event):
        print("[wxpython.py] OnClose called")
        if not self.browser:
            # May already be closing, may be called multiple times on Mac
            return

        if MAC:
            # On Mac things work differently, other steps are required
            self.browser.CloseBrowser()
            self.clear_browser_references()
            self.Destroy()
            global g_count_windows
            g_count_windows -= 1
            if g_count_windows == 0:
                cef.Shutdown()
                wx.GetApp().ExitMainLoop()
                # Call _exit otherwise app exits with code 255 (Issue #162).
                # noinspection PyProtectedMember
                os._exit(0)
        else:
            # Calling browser.CloseBrowser() and/or self.Destroy()
            # in OnClose may cause app crash on some paltforms in
            # some use cases, details in Issue #107.
            self.browser.ParentWindowWillClose()
            event.Skip()
            self.clear_browser_references()

    def clear_browser_references(self):
        # Clear browser references that you keep anywhere in your
        # code. All references must be cleared for CEF to shutdown cleanly.
        self.browser = None


class FocusHandler(object):
    def OnGotFocus(self, browser, **_):
        # Temporary fix for focus issues on Linux (Issue #284).
        if LINUX:
            print("[wxpython.py] FocusHandler.OnGotFocus:"
                  " keyboard focus fix (Issue #284)")
            browser.SetFocus(True)


class CefApp(wx.App):

    def __init__(self, redirect):
        self.timer = None
        self.timer_id = 1
        super(CefApp, self).__init__(redirect=redirect)

    def OnInit(self):
        self.create_timer()
        self.frame = MainFrame()
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

    def create_timer(self):
        # See also "Making a render loop":
        # http://wiki.wxwidgets.org/Making_a_render_loop
        # Another way would be to use EVT_IDLE in MainFrame.
        self.timer = wx.Timer(self, self.timer_id)
        self.timer.Start(10)  # 10ms timer
        wx.EVT_TIMER(self, self.timer_id, self.on_timer)

    def on_timer(self, _):
        cef.MessageLoopWork()

    def OnExit(self):
        self.timer.Stop()
        options.write_config()


if __name__ == '__main__':
    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    settings = {'remote_debugging_port': 2113,
                'context_menu': {'enabled': False}
                }
    if WINDOWS:
        # High DPI support
        settings["auto_zooming"] = "system_dpi"
        # noinspection PyUnresolvedReferences, PyArgumentList
        cef.DpiAware.SetProcessDpiAware()  # Alternative is to embed manifest
    cef.Initialize(settings=settings)
    app = CefApp(False)

    options = options.Options()
    JsHandler = jshandler.JsHandler(app)
    bindings = cef.JavascriptBindings(bindToFrames=True, bindToPopups=True)
    bindings.SetObject("Janet", JsHandler)
    bindings.SetProperty("config", core.CONFIG)

    app.frame.browser.SetJavascriptBindings(bindings)

    if core.CONFIG['start_fullscreen'] == 'true':
        app.frame.ShowFullScreen(True)

    app.MainLoop()
    del app  # Must destroy before calling Shutdown
    if not MAC:
        # On Mac shutdown is called in OnClose
        cef.Shutdown()
