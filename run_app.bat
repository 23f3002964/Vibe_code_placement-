@echo off
REM Script to run the Flask application

echo Starting the Placement Portal Flask Application...
set FLASK_APP=app.py
set FLASK_ENV=development

python -m flask run