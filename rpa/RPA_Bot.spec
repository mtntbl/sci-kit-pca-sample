# -*- mode: python ; coding: utf-8 -*-
# PyInstaller: pyinstaller --noconfirm --clean RPA_Bot.spec
# Klasör (onedir) derlemesi: Robot Framework kütüphaneleri ada göre dinamik yüklendiği için
# gerekli RPA/robot alt modülleri açıkça eklenir.
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs, collect_submodules

RPA_MODULLERI = (
    "RPA.Windows", "RPA.Desktop", "RPA.Browser.Selenium", "RPA.Browser.common", "RPA.Excel",
    "RPA.FileSystem", "RPA.PDF", "RPA.Tables", "RPA.core",
)


def guvenli(fn, *a, **k):
    try:
        return fn(*a, **k)
    except Exception as e:  # Windows'a özgü paketler Linux'ta yoktur
        print("atlandı:", a, e)
        return []


hidden = [
    "pca_rpa", "ayarlar", "belge_ocr", "ise_giris", "llm_katmani", "mcp_sunucu", "RpaBotKeywords",
    "ajan", "merkez_sunucu", "merkez_db", "merkez_panel", "merkez_istemci", "bildirim", "cron", "surecler",
    "kuyruk_isleri",
    "robot.libraries.BuiltIn", "robot.libraries.OperatingSystem", "robot.libraries.Collections",
    "robot.libraries.Process", "robot.libraries.String", "robot.libraries.DateTime",
    "robot.libraries.Screenshot", "robot.libraries.XML",
]
hidden += guvenli(collect_submodules, "robot")
hidden += guvenli(collect_submodules, "SeleniumLibrary")
hidden += guvenli(collect_submodules, "selenium")
hidden += guvenli(collect_submodules, "webdriver_manager")
hidden += guvenli(collect_submodules, "RPA", filter=lambda n: n.startswith(RPA_MODULLERI) or any(m.startswith(n + ".") for m in RPA_MODULLERI))
hidden += guvenli(collect_submodules, "uiautomation")
hidden += guvenli(collect_submodules, "comtypes")
hidden += guvenli(collect_submodules, "mcp", filter=lambda n: not n.startswith("mcp.cli"))
hidden += guvenli(collect_submodules, "anthropic")
for paket in ("uvicorn", "starlette", "anyio", "h11", "python_multipart", "multipart"):
    hidden += guvenli(collect_submodules, paket)

datas = []
for paket in ("robot", "SeleniumLibrary", "selenium", "webdriver_manager", "RPA", "uiautomation", "certifi", "mcp"):
    datas += guvenli(collect_data_files, paket)
binaries = []
for paket in ("uiautomation", "cv2", "pymupdf"):
    binaries += guvenli(collect_dynamic_libs, paket)

a = Analysis(
    ["rpa_bot.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden,
    excludes=["tkinter", "IPython", "jupyter", "notebook", "pytest"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="RPA_Bot", console=True, upx=False)
coll = COLLECT(exe, a.binaries, a.datas, name="RPA_Bot", upx=False)
