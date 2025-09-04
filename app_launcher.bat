@echo off
echo Starting EH MetalWorks QMS...
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
python app.py
pause
