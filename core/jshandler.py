from templates import index
import core
import json
from core import library, options
import logging
import wx
import os

'''
Layer between browser window and python backend

Takes javascript calls, runs backend code, and calls javascript method in DOM if required.

'''

desktop = os.path.join(os.path.expanduser('~'), 'Desktop')


class JsHandler(object):
    logging = logging.getLogger("JsHandler")

    def __init__(self, app):
        self.app = app
        self.browser = app.frame.browser
        self.options = options.Options()
        self.library = library.Library()

    # # # Interface handlers

    def toggle_fullscreen(self):
        if not self.app.frame.IsFullScreen():
            self.app.frame.ShowFullScreen(True)
        else:
            self.app.frame.ShowFullScreen(False)

    def exit(self):
        self.app.frame.Close()

    def loadindex(self):
        self.browser.ExecuteFunction('loadindex', index.render())

    # # # Library handlers

    def get_library(self):
        if core.LIBRARY:
            self.browser.ExecuteFunction('render_library', core.LIBRARY)
        else:
            logging.warning('Library empty or not found.')
        return

    def scan_library(self):
        self.browser.ExecuteFunction('render_library', self.library.scan())
        return

    def launch_game(self, rpx):
        err = self.library.launch_game(rpx)

        if err is not None:
            js = 'toastr.error("{}")'.format(err)
            self.browser.ExecuteJavascript(js)

    # # # Options handlers

    def set_option(self, key, value):
        core.CONFIG[key] = value

    def set_library_dir(self):
        dialog = wx.DirDialog(None, "Choose library directory", desktop, wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)

        dialog.ShowModal()
        library_directory = dialog.GetPath()

        if library_directory:
            core.CONFIG['library_directory'] = library_directory
            self.browser.ExecuteJavascript('$("input#library_directory").val({})'.format(json.dumps(library_directory)))

        dialog.Destroy()

    def set_cemu_exe(self):
        dialog = wx.FileDialog(None, "Open", desktop, "", "Cemu (*.exe)|*.exe", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)  # self.app.frame,

        dialog.ShowModal()
        cemu_exe = dialog.GetPath()

        if cemu_exe:
            core.CONFIG['cemu_exe'] = cemu_exe

            self.browser.ExecuteJavascript('$("input#cemu_exe").val({})'.format(json.dumps(cemu_exe)))

        dialog.Destroy()

    def set_bg_image(self):
        dialog = wx.FileDialog(None, "Open", desktop, "", "Images (*.jpg; *.png; *.bmp)|*.jpg; *.png; *.bmp", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        dialog.ShowModal()
        bg_image = dialog.GetPath()

        print bg_image

        if bg_image:
            core.CONFIG['background_image'] = bg_image

            self.browser.ExecuteJavascript('$("input#background_image").val({})'.format(json.dumps(bg_image)))
            self.browser.ExecuteFunction('update_bg_image', json.dumps(bg_image))

        dialog.Destroy()
