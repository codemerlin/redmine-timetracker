# -*- mode: python -*-
a = Analysis(['..\\..\main.py'],
             pathex=['M:\\projects\\rm.helpmetrack'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
a.datas += [('redmine_fluid_icon.gif','..\\..\\HelpMeTrack\\Resources\\redmine_fluid_icon.gif','DATA')]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='RmHelpMeTrack.exe',
          icon='..\\..\\HelpMeTrack\\Resources\\appicon.ico',
          debug=False,
          strip=None,
          upx=True,
          console=False , version='..\\file_version_info.txt')
