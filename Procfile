release: python manage.py migrate
web: python manage.py collectstatic --no-input; python manage.py create_group;
gunicorn news_website.wsgi --log-file -