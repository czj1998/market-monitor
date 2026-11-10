#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions 自动化数据更新与网页重写脚本
在 GitHub 云端执行：
1. 抓取隔夜最新美股行情与新闻
2. 运行科创50 (588000) 与 VIX 决策模型
3. 将最新量化数据注入 index.html 与 market_monitor_data.json
4. 如配置了 PUSHPLUS_TOKEN，同时发送微信推送
"""

import os
import sys
import json
import re
from strategy_scheduler import MarketScheduler, NotificationEngine, CONFIG

def main():
    print(">>> [1/4] 正在由 GitHub Actions 执行每日美股与科创50自动化推演...")
    
    # 1. 检查环境变量中的 Token (由 GitHub Secrets 注入)
    push_token = os.environ.get("PUSHPLUS_TOKEN", "")
    if push_token:
        CONFIG["NOTIFICATION"]["PUSHPLUS_TOKEN"] = push_token
        print(">>> [2/4] 已加载微信 PUSHPLUS_TOKEN 密钥")

    # 2. 运行策略引擎拉取最新数据
    scheduler = MarketScheduler()
    report = scheduler.run_strategy_pipeline()
    print(f">>> [3/4] 策略推演完成: 588000 决断 -> 【{report['star50_prediction']['verdict']}】")

    # 3. 将新数据彻底写回 index.html 和 market_monitor.html
    report_json_str = json.dumps(report, ensure_ascii=False, indent=2)

    for html_file in ["index.html", "market_monitor.html"]:
        if os.path.exists(html_file):
            with open(html_file, "r", encoding="utf-8") as f:
                content = f.read()

            # 替换或注入 <script id="embedded-data" type="application/json">
            tag_pattern = r'<script id="embedded-data" type="application/json">.*?</script>'
            replacement = f'<script id="embedded-data" type="application/json">\n{report_json_str}\n</script>'
            
            if re.search(tag_pattern, content, flags=re.DOTALL):
                content = re.sub(tag_pattern, replacement, content, flags=re.DOTALL)
            else:
                # 插入到 </head> 之前
                content = content.replace("</head>", f"  {replacement}\n</head>")

            with open(html_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f">>> [4/4] 成功将最新收盘数据写入 {html_file}")

    print(">>> 网页编译与数据更新完毕！")

if __name__ == "__main__":
    main()
