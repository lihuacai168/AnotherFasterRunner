@echo off
set input=%1

if "%input%"=="app" (
    echo start app
    set DJANGO_SETTINGS_MODULE=FasterRunner.settings.dev
    python manage.py runserver localhost:8000
)

