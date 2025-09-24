# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file for TJM Automation Bot
This file defines how to build the standalone executable.
"""

import os
from pathlib import Path

# Get the current directory
current_dir = Path.cwd()

# Define the main script
main_script = current_dir / 'bot.py'

# Define the output directory
output_dir = current_dir / 'dist'

# Define the build directory
build_dir = current_dir / 'build'

# Define the application name
app_name = 'TJM_Automation_Bot'

# Analysis configuration
a = Analysis(
    [str(main_script)],
    pathex=[str(current_dir)],
    binaries=[],
    datas=[
        # Include any additional data files if needed
        # ('path/to/data', 'data'),
    ],
    hiddenimports=[
        'pyautogui',
        'pygetwindow',
        'requests',
        'pathlib',
        'logging',
        'subprocess',
        'time',
        'os',
        'sys',
        'typing',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# PYZ configuration
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# EXE configuration
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False to hide console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    version=1.0.0,
)
