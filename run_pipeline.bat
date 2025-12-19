@echo off
setlocal

REM ---- Go to project directory ----
cd /d "C:\Users\Rudra\Documents\Retail Price Tracking"

REM ---- Activate virtual environment ----
call venv\Scripts\activate

REM ---- Run pipeline and capture logs ----
python main.py > pipeline_log.txt 2>&1

REM ---- Explicitly exit cmd ----
exit /b 0