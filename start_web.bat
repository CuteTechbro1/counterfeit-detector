@echo off
echo ===================================================
echo Starting Counterfeit Detector Web Platform...
echo ===================================================
cd /d "%~dp0services\api"
set PYTHONPATH=.;..\..\packages
.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
