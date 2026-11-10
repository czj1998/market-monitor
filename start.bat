@echo off
chcp 65001 >nul
title 美股量化监控与科创50决策终端
echo 正在检查 Python 环境并启动终端...
python run_daily.py
if %errorlevel% neq 0 (
    echo.
    echo [提示] 启动失败，请检查是否已安装 Python 3 并添加到系统环境变量。
    pause
)
