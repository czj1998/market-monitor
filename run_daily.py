#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
======================================================================
美股与科创50决策终端 · 本地一键启动伴侣 (run_daily.py)
功能：
1. 启动时自动从 Yahoo Finance API 抓取最新美股/VIX/科技股与要闻数据。
2. 运行量化推演引擎，更新前端数据。
3. 自动在本地启动微型轻量服务，避免浏览器跨域(CORS)问题。
4. 自动唤起你的默认浏览器打开仪表盘网页。
======================================================================
"""

import os
import sys
import json
import time
import webbrowser
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

# 导入同目录下的定时策略引擎
try:
    from strategy_scheduler import MarketScheduler, CONFIG
except ImportError:
    print("错误: 请确保 strategy_scheduler.py 与本脚本位于同一文件夹下。")
    sys.exit(1)

PORT = 8899

class CustomHandler(SimpleHTTPRequestHandler):
    """静默处理静态文件请求"""
    def log_message(self, format, *args):
        # 屏蔽控制台刷屏日志，保持界面干净
        pass

def start_server():
    server = HTTPServer(('127.0.0.1', PORT), CustomHandler)
    server.serve_forever()

def main():
    print("=" * 60)
    print("  🚀 正在启动【美股量化全景与科创50决策终端】本地服务...")
    print("=" * 60)
    
    # 1. 立即执行一次最新数据抓取与推演
    print("[1/3] 正在通过 Yahoo Finance API 拉取隔夜最新美股行情与要闻...")
    scheduler = MarketScheduler()
    report = scheduler.run_strategy_pipeline()
    
    vix = report["vix_analysis"]
    star50 = report["star50_prediction"]
    print(f"      ✔ 恐慌指数 VIX: {vix['vix_value']} ({vix['state']})")
    print(f"      ✔ 次日科创50 (588000) 决断: 【{star50['verdict']}】")
    print(f"      ✔ 预期集合竞价开盘缺口: {star50['expected_open_gap_pct']}")

    # 2. 检查 html 文件
    html_target = "market_monitor.html"
    if not os.path.exists(html_target):
        # 如果放在 artifacts 目录则尝试复制或提示
        alt_path = os.path.join("artifacts", "file_generation", "ttl=63d", "output", "market_monitor.html")
        if os.path.exists(alt_path):
            import shutil
            shutil.copy(alt_path, html_target)

    # 3. 后台启动本地轻量 Web 服务
    print(f"[2/3] 正在启动本地服务: http://127.0.0.1:{PORT}/ ...")
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(1)

    # 4. 自动打开浏览器
    target_url = f"http://127.0.0.1:{PORT}/{html_target}"
    print(f"[3/3] 正在唤起默认浏览器打开仪表盘: {target_url}")
    webbrowser.open(target_url)

    print("=" * 60)
    print(f"  ✨ 仪表盘已成功在浏览器中打开！")
    print(f"  📌 访问地址: {target_url}")
    print(f"  💡 提示: 保持此窗口开启即可持续提供服务，按 Ctrl+C 可退出。")
    print("=" * 60)

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("\n本地服务已安全停止。")

if __name__ == "__main__":
    main()
