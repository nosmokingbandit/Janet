import logging
import core
import os
import json

cwd = os.getcwd()

config_template = {"library_directory": "",
                   "cemu_exe": "",
                   "scan_on_load": "false",
                   "start_maximized": "false",
                   "start_fullscreen": "false",
                   "cemu_fullscreen": "false",
                   "game_image_size": 100,
                   "library_style": "banner",
                   "background_image": ""
                   }


class Options(object):
    logging = logging.getLogger("Options")

    def __init__(self):
        self.config_path = os.path.join(cwd, 'config.json')
        if not core.CONFIG:
            core.CONFIG = self.open_config()
        return

    def open_config(self):
        if not os.path.isfile(self.config_path):
            logging.info('Creating new config file.')
            print 'Creating new config file.'
            core.CONFIG = config_template
            self.write_config()
            return config_template
        else:
            logging.info('Found config file.')
            print 'Reading config file {}'.format(self.config_path)
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            return config

    def set_config(self, key, value):
        ''' Sets core.CONFIG['key'] = value
        '''

        core.CONFIG[key] = value
        return

    def write_config(self):
        ''' Writes core.CONFIG to file
        '''
        try:
            with open(self.config_path, 'w+') as f:
                json.dump(core.CONFIG, f, indent=2)
            logging.info('Saved config.json')
            return True
        except Exception, e: #noqa
            logging.error(str(e), exc_info=True)
            return False
