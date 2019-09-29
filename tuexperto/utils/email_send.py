from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

def email_send(template_name, context, mail_subject, to_email):
	mail_subject = mail_subject
	html_content = render_to_string(template_name , context)

	email = EmailMultiAlternatives(mail_subject, "")
	email.attach_alternative(html_content, "text/html")
	email.to = to_email
	email.send()