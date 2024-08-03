#!bin/bash

echo <<<<<<<<<<<<<<<creating migration files>>>>>>>>>>>>>>>>>>>
python -m manage makemigrations --no-input
echo <<<<<<<<<<<<<<<<<<running migrations>>>>>>>>>>>>>>>>>>>>>>
python -m manage migrate --no-input
echo <<<<<<<<<<<<<<<collecting static files>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
python -m manage collectstatic --no-input
echo <<<<<<<<<<<<<<<<<<<<starting server>>>>>>>>>>>>>>>>>>>>>>>
gunicorn src.settings.wsgi:application --bind 0.0.0.0:7000