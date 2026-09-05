# -*- mode: python ; coding: utf-8 -*-
"""招聘AI助手 最新版打包配置（launcher.py 入口，console 模式）
覆盖：FastAPI 后端(8010) + app.py 前端(7860) + 多用户登录 + 文档上传解析 + AI 对话
"""
from PyInstaller.utils.hooks import collect_all

datas = []
binaries = []
hiddenimports = []
for pkg in ['openpyxl', 'uvicorn', 'pydantic', 'pypdf', 'docx', 'pandas',
            'openai', 'fastapi', 'lxml', 'anyio', 'httpx']:
    tmp = collect_all(pkg)
    datas += tmp[0]
    binaries += tmp[1]
    hiddenimports += tmp[2]

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['gradio', 'matplotlib', 'tkinter'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='招聘AI助手',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='招聘AI助手',
)
