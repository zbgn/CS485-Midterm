# -*- mode: python -*-

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=['/Users/gysco/CSUSM/CS485/CS485-Midterm'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher)
a.datas += Tree('./img/', prefix='./img/') + Tree('./font/', prefix='./font/')
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='Gomoku',
    debug=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=True,
    icon='img/gomoku.icns')
app = BUNDLE(
    exe, name='Gomoku.app', icon='./img/gomoku.icns', bundle_identifier=None)
