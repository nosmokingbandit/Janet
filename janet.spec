# -*- mode: python -*-

block_cipher = None


# Get cef directory
from cefpython3 import cefpython
import os
cef_path = os.path.dirname(cefpython.__file__)

include_files = [('static\\', 'static\\'),
                 ('templates\\', 'templates\\'),
                 (cef_path+'\\icudtl.dat', '.'),
                 (cef_path+'\\locales', 'locales\\'),
                 (cef_path+'\\natives_blob.bin', '.'),
                 (cef_path+'\\cef.pak', '.'),
                 (cef_path+'\\cef_100_percent.pak', '.'),
                 (cef_path+'\\cef_200_percent.pak', '.'),
                 (cef_path+'\\cef_extensions.pak', '.'),
                 (cef_path+'\\libEGL.dll', '.'),
                 (cef_path+'\\libGLESv2.dll', '.'),
                 (cef_path+'\\natives_blob.bin', '.'),
                 (cef_path+'\\subprocess.exe', '.')
                 ]

a = Analysis(['janet.py'],
             pathex=['C:\\Users\\Steven\\Desktop\\Janet'],
             binaries=[],
             datas=include_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='janet',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='janet')
