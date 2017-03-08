from lib import htmlPy
import os
import json
import xml.etree.cElementTree as ET
import core
import subprocess
import threading
from PIL import Image

import logging

cwd = os.getcwd()


class BackEnd(htmlPy.Object):

    def __init__(self, app):
        super(BackEnd, self).__init__()
        self.app = app


class Gui(htmlPy.Object):
    def __init__(self, app):
        super(Gui, self).__init__()
        self.app = app
        return

    @htmlPy.Slot()
    def toggle_fullscreen(self):
        if self.app.window.isFullScreen():
            self.app.window.showNormal()
        else:
            self.app.window.showFullScreen()

    @htmlPy.Slot()
    def close_window(self):
        self.app.window.close()


class Options(htmlPy.Object):
    logging = logging.getLogger("Options")

    def __init__(self, app):
        super(Options, self).__init__()
        self.app = app

        self.config_template = {"library_directory": "",
                                "cemu_exe": "",
                                "scan_on_load": "false",
                                "start_maximized": "false",
                                "start_fullscreen": "false",
                                "cemu_fullscreen": "false"
                                }
        self.config_path = os.path.join(cwd, 'config.json')
        core.CONFIG = self.open_config()
        return

    def open_config(self):
        if not os.path.isfile(self.config_path):
            logging.info('Creating new config file.')
            self.write_config(json.dumps(self.config_template))
            return self.config_template
        else:
            logging.info('Found config file.')
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            return config

    @htmlPy.Slot(result=str)
    def get_config(self):
        return json.dumps(core.CONFIG)

    @htmlPy.Slot(str)
    def log(self, x):
        print x
        logging.info(x)

    @htmlPy.Slot(str, result=bool)
    def write_config(self, config):
        conf = json.loads(config)
        try:
            with open(self.config_path, 'w+') as f:
                json.dump(conf, f, indent=2)
            core.CONFIG = conf
            logging.info('Saved config.json')
            return True
        except Exception, e: #noqa
            logging.error(str(e), exc_info=True)
            return False


class Library(htmlPy.Object):
    logging = logging.getLogger("Library")

    def __init__(self, app):
        super(Library, self).__init__()
        self.app = app
        if core.CONFIG.get('library_directory'):
            library_json = os.path.join(cwd, 'library.json')
            if os.path.isfile(library_json):
                logging.info('Found existing library.')
                with open(library_json) as f:
                    core.LIBRARY = json.load(f)

        self.images_dir = os.path.join(cwd, 'game_images')
        if not os.path.isdir(self.images_dir):
            os.mkdir(self.images_dir)

        return

    @htmlPy.Slot(result=str)
    def get_library(self):
        if core.LIBRARY:
            return json.dumps(core.LIBRARY)
        else:
            return "[]"

    @htmlPy.Slot(result=str)
    def scan(self):
        logging.info('Scanning library.')
        library_dir = core.CONFIG['library_directory']

        game_data = []
        gamedirs = [os.path.join(library_dir, i) for i in os.listdir(library_dir) if os.path.isdir(os.path.join(library_dir, i))]

        for i in gamedirs:
            game = {}

            game['directory'] = i

            # Parse meta xml for name, game id
            xml = os.path.join(i, 'meta', 'meta.xml')
            try:
                with open(xml) as f:
                    xml_root = ET.fromstring(f.read())
                    for elem in xml_root:
                        if elem.tag == 'product_code':
                            game['game_id'] = elem.text.split('-')[-1] + '01'
                        if elem.tag == 'shortname_en':
                            game['title'] = elem.text.title()
            except Exception, e: #noqa
                logging.error(str(e), exc_info=True)
                continue

            # get name of rpx binary
            for f in os.listdir(os.path.join(i, 'code')):
                if os.path.splitext(f)[1] == '.rpx':
                    game['binary'] = os.path.join(i, 'code', f)
                    break

            # get cover image
            img = os.path.join(self.images_dir, '{}.jpg'.format(game['game_id']))
            if not os.path.isfile(img):
                self.app.evaluate_javascript('toastr.info("Converting title image for {}")'.format(game['game_id']))
                t = threading.Thread(target=self.get_image, args=(game,))
                t.start()

            game_data.append(game)

        logging.info('Storing library.json')
        with open(os.path.join(cwd, 'library.json'), 'w') as f:
            json.dump(game_data, f, indent=2, sort_keys=True)

        self.app.evaluate_javascript('toastr.success("Found {} games")'.format(len(game_data)))
        return json.dumps(game_data)

    def get_image(self, game):
        logging.info('Converting title image for {}.'.format(game['game_id']))
        title_tga = os.path.join(game['directory'], 'meta', 'bootTvTex.tga')
        title_jpg = os.path.join(self.images_dir, '{}.jpg'.format(game['game_id']))
        icon_tga = os.path.join(game['directory'], 'meta', 'iconTex.tga')
        icon_jpg = os.path.join(self.images_dir, '{}_icon.jpg'.format(game['game_id']))
        try:
            title = Image.open(title_tga)
            title.thumbnail((640, 360))
            title.save(title_jpg)

            Image.open(icon_tga).save(icon_jpg)
        except Exception, e:
            logging.error(str(e), exc_info=True)
        return

    @htmlPy.Slot(str, result=bool)
    def launch_game(self, rpx):
        # "programs\cemu.exe" -g "Title\code\title.rpx" -f
        cemu = core.CONFIG['cemu_exe']

        command = [cemu, '-g', rpx]

        if core.CONFIG['cemu_fullscreen'] == "true":
            command.append('-f')

        logging.info('Launching title:')
        logging.info(' '.join(command))
        try:
            subprocess.Popen(command,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             shell=False
                             )
            return True
        except Exception, e: #noqa
            self.app.evaluate_javascript('toastr.error("{}")').format(str(e))
            logging.error(str(e), exc_info=True)
            return False
