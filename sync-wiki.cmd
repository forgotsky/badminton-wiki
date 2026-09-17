@echo off
chcp 65001 >nul
echo ==========================================
echo   羽毛球 wiki 一键同步
echo   把 vault 里的羽毛球笔记同步到 wiki 并部署
echo ==========================================
python "%~dp0sync_wiki.py"
echo.
pause
