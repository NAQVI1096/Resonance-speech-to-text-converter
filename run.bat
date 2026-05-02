@echo off
echo ==============================================
echo    Starting AudioScribe Backend Server...
echo ==============================================
start cmd /k "uvicorn main:app --reload --port 8000"

timeout /t 5 /nobreak >nul

echo ==============================================
echo    Starting AudioScribe Frontend Server...
echo ==============================================
start cmd /k "streamlit run app.py"

echo Both servers are starting up. Close these command prompt windows to stop the servers.
pause
