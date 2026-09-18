@echo off
chcp 65001 >nul
echo ==========================================
echo   羽毛球 wiki 部署到腾讯云 COS
echo   （需要先 pip install coscmd 并 coscmd config 配置好）
echo ==========================================
python "%~dp0deploy_tencent.py"
echo.
pause
