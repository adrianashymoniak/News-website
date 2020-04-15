release: python manage.py migrate; python manage.py create_group
web: python manage.py collectstatic --no-input; gunicorn news_website.wsgi --log-file -