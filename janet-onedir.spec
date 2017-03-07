# -*- mode: python -*-

block_cipher = None

include_files = [('lib\\htmlPy\\binder.js', 'lib\\htmlPy\\'),
				 ('static\\', 'static\\'),
				 ('templates\\', 'templates\\')
				 ]
a = Analysis(['janet.py'],
             pathex=[''],
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
