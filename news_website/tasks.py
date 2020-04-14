from django.core.mail import EmailMessage

from news_website.celery import app


@app.task
def send_email(mail_subject, message, from_email, to_email):
    msg = EmailMessage(mail_subject, message, from_email, to_email)
    msg.content_subtype = 'html/txt'
    msg.send()
