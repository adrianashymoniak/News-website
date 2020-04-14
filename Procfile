release: python manage.py migrate
web: python manage.py collectstatic --no-input; gunicorn news_website.wsgi --log-file -