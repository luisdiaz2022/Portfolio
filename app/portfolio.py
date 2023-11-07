from flask import (
    Blueprint, render_template, request, current_app
)

from email.message import EmailMessage
import ssl
import smtplib
from email.mime.text import MIMEText

bp = Blueprint('portfolio', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    return render_template('portfolio/index.html')

@bp.route('/mail', methods=['GET','POST'])
def mail():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if request.method == 'POST':
        send_email(name, email, message)
        return render_template('portfolio/sent_mail.html')

    return render_template('portfolio/sent_mail.html')

def send_email(name, email, message):
    my_email = current_app.config['FROM_EMAIL']
    email_key = current_app.config['GOOGLE_KEY']
    email_to = email
    email_message = MIMEText(message, 'plain')
    email_name = name
    email_subject = 'Correo de ' + email_name

    email_sender = EmailMessage()
    email_sender['From'] = my_email
    email_sender['To'] = email_to
    email_sender['subject'] = email_subject
    email_sender.set_content(email_message)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(my_email, email_key)
        smtp.sendmail(my_email, email_to, email_sender.as_string())