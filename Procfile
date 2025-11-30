web: gunicorn hishamAiAgentOS.wsgi --bind 0.0.0.0:$PORT --workers 4 --threads 2 --timeout 120 --log-file - --access-logfile - --error-logfile - --log-level info
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput --clear
worker: celery -A hishamAiAgentOS worker --loglevel=info
beat: celery -A hishamAiAgentOS beat --loglevel=info
