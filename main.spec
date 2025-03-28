# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[('src/api', 'api')],
    hiddenimports=[
        'api',
        'api.core',
        'api.core.schemas',
        'api.core.exceptions',
        'api.api_router',
        'api.api_router.tianyi_tasks.api',
        'api.api_router.port_manager.api',
        'api.api_router.example.api',
        'api.api_router.example2.api'
    ],
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
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
