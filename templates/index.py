import core
import dominate
from dominate.tags import *
import json


def render():
    doc = dominate.document(title='Janet')

    with doc.head:
        meta(name='cwd', content=core.BASE_DIR)

        link(rel='stylesheet', href=core.BASE_DIR + '/static/css/style.css')
        link(rel='stylesheet', href=core.BASE_DIR + '/static/css/ionicons.css')
        link(rel='stylesheet', href=core.BASE_DIR + '/static/css/toastr.css')
        link(rel='stylesheet', href=core.BASE_DIR + '/static/css/varela.css')

        script(type='text/javascript', src=core.BASE_DIR + '/static/js/jquery-3.1.1.min.js')
        script(type='text/javascript', src=core.BASE_DIR + '/static/js/jquery-ui.min.js')
        script(type='text/javascript', src=core.BASE_DIR + '/static/js/main.js')
        script(type='text/javascript', src=core.BASE_DIR + '/static/js/library.js')
        script(type='text/javascript', src=core.BASE_DIR + '/static/js/options.js')
        script(type='text/javascript', src=core.BASE_DIR + '/static/js/toastr.js')
        script('toastr.options.positionClass = "toast-bottom-right"; toastr.options.preventDuplicates = false; toastr.options.timeOut = 2000;', type='text/javascript')

    with doc:
        with ul(id='menu_bar'):
            with li(id='options_button'):
                i(cls='icon ion-android-settings')
                span('Options')
            with li(id='scan_library'):
                i(cls='icon ion-refresh')
                span('Re-Scan Library')

            if core.CONFIG['start_fullscreen'] == 'true':
                with li(id='close_window', cls='window_control'):
                    i(cls='icon ion-close')
                with li(id='toggle_fullscreen', cls='window_control', fullscreen='true'):
                    i(cls='icon ion-android-contract')
            else:
                with li(id='close_window', cls='window_control hidden'):
                    i(cls='icon ion-close')
                with li(id='toggle_fullscreen', cls='window_control', fullscreen='false'):
                    i(cls='icon ion-android-expand')

        with div(id='library_size_wrapper', style='font-size: {}%'.format(core.CONFIG['game_image_size'])):
            ul(id='library', cls=core.CONFIG['library_style'], scan=core.CONFIG['scan_on_load'])

        with ul(id='ui_bar'):
            with li(id='toggle_display'):
                if core.CONFIG['library_style'] == 'banner':
                    i(cls='icon ion-ios-grid-view', title='Toggle game disply style')
                else:
                    i(cls='icon ion-grid', title='Toggle game disply style')
            with li(id='display_slider'):
                div(id='slider')
            with li(id='gamepad'):
                i(cls='icon ion-ios-game-controller-a-outline')

        cfg = core.CONFIG
        with div(id='options'):
            with ul(id='options_list'):
                with li():
                    p('Library directory:')
                    with button(onClick='Janet.set_library_dir()'):
                        i(cls='icon ion-android-folder')
                    input(type='text', disabled='disabled', id='library_directory', value=cfg['library_directory'])
                with li():
                    i(cls='icon ion-android-checkbox-outline-blank checkbox', name='scan_on_load', value=cfg['scan_on_load'])
                    span('Scan library when opening Janet.')
                with li():
                    i(cls='icon ion-android-checkbox-outline-blank checkbox', name='start_fullscreen', value=cfg['start_fullscreen'])
                    span('Start Janet in fullscreen mode.')
                with li():
                    p('Background image:')
                    with button(onClick='Janet.set_bg_image()'):
                        i(cls='icon ion-android-folder')
                    input(type='text', disabled='disabled', id='background_image', value=cfg['background_image'])
                with li():
                    p('Path to Cemu.exe:')
                    with button(onClick='Janet.set_cemu_exe()'):
                        i(cls='icon ion-android-folder')
                    input(type='text', disabled='disabled', id='cemu_exe', value=cfg['cemu_exe'])
                with li():
                    i(cls='icon ion-android-checkbox-outline-blank checkbox', name='cemu_fullscreen', value=cfg['cemu_fullscreen'])
                    span('Launch Cemu in fullscreen mode.')

        div(id='loading')

    if core.CONFIG['background_image']:
        doc.body['style'] = 'background-image: url({})'.format(json.dumps(core.CONFIG['background_image']))

    return doc.render()

# pylama:ignore=W0401
