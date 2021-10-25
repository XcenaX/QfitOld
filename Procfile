web: daphne qfit.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=qfit.settings -v2
clock: python points.py