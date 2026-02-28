@echo off
CHCP 65001 >nul
cd /d "%~dp0"
echo ===================================================
echo   每日投資資訊彙整與通知系統啟動
echo ===================================================
if not exist ".venv\Scripts\python.exe" (
    echo [警告] 找不到虛擬環境 (.venv)。請確認是否已安裝 Python。
    echo 將嘗試使用全系統 Python 執行...
    python main.py
) else (
    .\.venv\Scripts\python main.py
)
echo.
pause
