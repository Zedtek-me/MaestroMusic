#!bin/bash

echo "<<<<<<<<<<<<<<<creating migration files>>>>>>>>>>>>>>>>>>>"
python -m manage makemigrations --no-input
echo "<<<<<<<<<<<<<<<<<<running migrations>>>>>>>>>>>>>>>>>>>>>>"
python -m manage migrate --no-input
echo "<<<<<<<<<<<<<<<collecting static files>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
python -m manage collectstatic --no-input
echo "<<<<<<<<<<<<<<<<<<<<starting server>>>>>>>>>>>>>>>>>>>>>>>"
python -m manage runserver 0.0.0.0:7000

# gunicorn --workers 2 -t 5 src.wsgi:application --bind 0.0.0.0:7000