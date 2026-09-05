# -*- coding: utf-8 -*-
"""招聘AI助手 启动器（打包 exe 用）
一键同时启动：后端接口(8010) + 单页前端(7860)，并自动打开浏览器。
打包为 exe 后，.env 配置文件与 data/ 台账放在 exe 同目录即可。"""
import multiprocessing
import os
import sys
import threading
import time


def _resource_dir():
    """exe 所在目录（onefile 运行时即 sys.executable 目录）"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def _log(msg):
    try:
        with open(os.path.join(_resource_dir(), "招聘AI助手.log"), "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    except Exception:
        pass


def _error_box(msg):
    _log("ERROR: " + msg)
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("招聘AI助手", msg)
    except Exception:
        pass


def _wait_backend(url, timeout=40):
    import requests
    for _ in range(int(timeout / 0.3)):
        try:
            requests.get(url, timeout=1)
            return True
        except Exception:
            time.sleep(0.3)
    return False


def main():
    multiprocessing.freeze_support()
    os.chdir(_resource_dir())
    # 数据目录指向 exe 同目录的 data/（含用户账号与台账），源码运行时无此变量用默认 data/
    os.environ["RECRUIT_DATA_DIR"] = os.path.join(_resource_dir(), "data")
    _log("启动中...")

    # 加载后端（同时校验 .env）
    try:
        from recruit_ai_qwen38 import app
    except Exception as e:
        _error_box(f"初始化失败：{e}\n\n请确认 exe 同目录下有 .env 文件，且已配置\nLLM_BASE_URL / LLM_API_KEY / LLM_MODEL。")
        return

    # 后端服务线程
    def run_backend():
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8010, log_level="warning")

    threading.Thread(target=run_backend, daemon=True).start()

    if not _wait_backend("http://127.0.0.1:8010/docs"):
        _error_box("后端启动超时，请检查 .env 配置是否正确。")
        return

    _log("后端就绪，启动前端...")

    # 前端（阻塞运行，自动打开浏览器）
    try:
        import webbrowser
        webbrowser.open("http://127.0.0.1:7860")
        import uvicorn
        import app as frontend_app
        uvicorn.run(frontend_app.app, host="127.0.0.1", port=7860)
    except Exception as e:
        _error_box(f"前端启动失败：{e}\n\n若 7860 端口被占用，请关闭占用程序后重试。")


if __name__ == "__main__":
    main()
