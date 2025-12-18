@echo off

REM ---- Go to project directory ----
cd /d "C:\Users\Rudra\Documents\Retail Price Tracking"

REM ---- Activate virtual environment ----
call venv\Scripts\activate

REM ---- Run the pipeline ----
python main.py

REM ---- Keep window open for logs (optional) ----
pause
