# -*- mode: python -*-
a = Analysis(['First.py'],
             pathex=['/home/mthakral/projects/rm.helpmetrack'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='First',
          debug=False,
          strip=None,
          upx=True,
          console=False , version='file_version_info.txt')
