# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['ReportINC_GUI.py'],
             pathex=['E:\\MOOCs\\My Projects\\ReportINC'],
             binaries=[],
             datas=[("E:\\MOOCs\\My Projects\\ReportINC\\venv\\Lib\\site-packages\\tinycss2\\VERSION", "tinycss2"),
			 ("E:\\MOOCs\\My Projects\\ReportINC\\venv\\Lib\\site-packages\\cssselect2\\VERSION", "cssselect2"),
			 ("E:\\MOOCs\\My Projects\\ReportINC\\logo\\taskbar-icon.ico", ".")],
             hiddenimports=["tinycss2", "cssselect2"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='ReportINC_GUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon="E:\\MOOCs\\My Projects\\ReportINC\\logo\\taskbar-icon.ico")
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='ReportINC_GUI')
