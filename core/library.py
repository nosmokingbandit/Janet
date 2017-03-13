import logging
import os
import json
import core
import xml.etree.cElementTree as ET
import subprocess
import threading
from PIL import Image

cwd = os.getcwd()


class Library(object):
    logging = logging.getLogger("Library")

    def __init__(self):
        if core.CONFIG.get('library_directory'):
            library_json = os.path.join(cwd, 'library.json')
            if os.path.isfile(library_json):
                logging.info('Loaded existing library:')
                logging.info(library_json)
                print library_json
                with open(library_json) as f:
                    core.LIBRARY = json.load(f)

        self.images_dir = os.path.join(cwd, 'game_images')
        if not os.path.isdir(self.images_dir):
            os.mkdir(self.images_dir)

        return

    def scan(self):
        logging.info('Scanning library.')
        library_dir = core.CONFIG['library_directory']

        if not os.path.isdir(library_dir):
            return

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
                t = threading.Thread(target=self.get_image, args=(game,))
                t.start()

            game_data.append(game)

        logging.info('Storing library.json')
        with open(os.path.join(cwd, 'library.json'), 'w') as f:
            json.dump(game_data, f, indent=2, sort_keys=True)

        return game_data

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
            return None
        except Exception, e: #noqa
            logging.error(str(e), exc_info=True)
            return str(e)
