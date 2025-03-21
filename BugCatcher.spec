# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['bug-catching-cat.py'],
    pathex=['/Users/ericgoodman/Repo/bugCatcherGame'],
    binaries=[],
    datas=[('/Users/ericgoodman/Repo/bugCatcherGame/assets', 'assets'), ('/Users/ericgoodman/Repo/bugCatcherGame/src', 'src')],
    hiddenimports=['pygame', 'src.game', 'src.sprites.player', 'src.sprites.bug', 'src.utils.constants', 'src.utils.leaderboard', 'src.utils.image_processor'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('v', None, 'OPTION')],
    name='BugCatcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='BugCatcher.app',
    icon=None,
    bundle_identifier=None,
)
