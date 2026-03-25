# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for AI Prompt Generator Pro

import os
import sys

# Application information
APP_NAME = "PromptGeneratorPro"
APP_ICON = "assets/icons/app_icon.ico"
MAIN_SCRIPT = "prompt_generator.py"
VERSION_FILE = "version_info.py"

# Get absolute paths
spec_dir = os.path.dirname(os.path.abspath(SPEC))
icon_path = os.path.join(spec_dir, APP_ICON)

# Data files to include
added_files = [
    (os.path.join(spec_dir, 'templates'), 'templates'),
    (os.path.join(spec_dir, 'assets/icons'), 'assets/icons'),
]

# Hidden imports (modules that PyInstaller might miss)
hidden_imports = [
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'PyQt6.sip',
    'pandas',
    'numpy',
    'numpy.core._multiarray_umath',
    'pandas._libs.tslibs.timedeltas',
    'pandas._libs.tslibs.nattype',
    'pandas._libs.tslibs.np_datetime',
    'pandas._libs.skiplist',
    'json',
    'uuid',
    'datetime',
    'pathlib',
    're',
    'os',
    'sys',
]

# Analysis configuration
a = Analysis(
    [MAIN_SCRIPT],
    pathex=[spec_dir],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'scipy',
        'IPython',
        'jupyter',
        'pytest',
        'black',
        'flake8',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Remove unnecessary modules to reduce size
a.binaries = [x for x in a.binaries if not x[0].startswith('matplotlib')]
a.binaries = [x for x in a.binaries if not x[0].startswith('scipy')]

# PYZ configuration
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# EXE configuration for single-file executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
    version=VERSION_FILE,
)

# For directory-based distribution (optional)
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name=APP_NAME,
# )