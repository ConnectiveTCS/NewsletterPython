# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Newsletter Application
"""

block_cipher = None

# Collect all data files
a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('instance', 'instance'),
        ('*.py', '.'),
        ('requirements.txt', '.'),
        ('README.md', '.'),
        ('*.md', '.'),
        ('*.csv', '.'),
    ],
    hiddenimports=[
        'flask',
        'flask_sqlalchemy', 
        'flask_migrate',
        'sqlite3',
        'email.mime.text',
        'email.mime.multipart',
        'smtplib',
        'unicodedata',
        'threading',
        'logging',
        'datetime',
        'os',
        'sys',
        'werkzeug.security',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NewsletterApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)