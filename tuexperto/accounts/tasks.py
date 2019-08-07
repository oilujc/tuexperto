import string

from django.utils.crypto import get_random_string
from celery import shared_task

from datetime import datetime, timedelta, time
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.contrib.auth import get_user_model, authenticate, login
from utils.tokens import account_activation_token

@shared_task
def send_msg(user, current_site):
	try:
		user = get_user_model().objects.get(pk = user)
		uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()

		mail_subject = 'Activate your account.'
		message = render_to_string('auth/email_confirm_template.html', {
			'mail_subject': mail_subject,
	         'user': user,
	         'domain': current_site,
	         'uid':uid,
	         'token':account_activation_token.make_token(user),
	     })
		to_email = user.email

		email = EmailMultiAlternatives(mail_subject, "", "postmaster@girosapp.com", [to_email])
		email.attach_alternative(message, "text/html")
		email.send()

	except get_user_model().DoesNotExist:
		print("Error to get user")

	