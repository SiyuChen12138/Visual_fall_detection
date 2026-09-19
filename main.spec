# -*- mode: python ; coding: utf-8 -*-
#
# 行人跌倒检测系统 —— PyInstaller 打包配置
# Copyright (C) 2026 SiyuChen12138
# 本文件以 GNU General Public License v3.0 发布，完整许可文本见 LICENSE。


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('runs/train/exp4/weights/best.pt', 'runs/train/exp4/weights'), ('utils/*', 'utils')],
    hiddenimports=['detect', 'torch', 'torchvision', 'cv2'],
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
    runtime_tmpdir='.',
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
