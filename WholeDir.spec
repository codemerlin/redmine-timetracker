# -*- mode: python -*-
a = Analysis(['.\\tkinter_main.py'],
             pathex=['M:\\projects\\rm.helpmetrack'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
a.datas += [('appicon.ico','appicon.ico','DATA')]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='First.exe',
          icon='appicon.ico',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='First')
