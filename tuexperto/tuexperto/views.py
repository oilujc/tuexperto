from .forms import SignupForm
from datetime import datetime, timedelta, time
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import (
    TemplateView, FormView, ListView, DetailView, View)
from meta.views import MetadataMixin
from utils.tokens import account_activation_token
from blog.models import Post
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from .settings import TITLE_PAGE, GLOBAL_DESCRIPTION

# Create your views here.


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    context = {'title_page': 'Registrarse',
               'breadcrumb': [(reverse_lazy('home'), 'Inicio'), ('', 'Registrarse')]}

    form = SignupForm(request.POST or None)
    context["form"] = form
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # context["success_msg"] = "Your account has been created successfully. Wait for an administrator to activate your account"

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta.'
            html_content = render_to_string('auth/email_confirm_template.html', {
                'mail_subject': mail_subject,
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'contactEmail': 'support@tuexperto.pro',
                'companyName': 'TuExperto.pro',
                'token': account_activation_token.make_token(user),
            })
            to_email = user.email

            email = EmailMultiAlternatives(mail_subject, "")
            email.attach_alternative(html_content, "text/html")
            email.to = [to_email]
            email.send()

            context["success_msg"] = "Please confirm your email address to complete the registration"

    else:
        form = SignupForm()

    return render(request, 'auth/signup.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')


class HomeView(MetadataMixin, TemplateView):
    template_name = 'home.html'

    title = TITLE_PAGE
    description = GLOBAL_DESCRIPTION

    keywords=['blog', 'informacion', 'increible', 'desarrollo web', 'desarrollo', 'website', 'develop', 'desarrollador']

    extra_props = {
	    'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
	   	}
    extra_custom_props=[
	    ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
	   	]

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        return context


class ContactFormView(MetadataMixin, TemplateView):
    template_name = "contact/index.html"

    title = TITLE_PAGE
    description = GLOBAL_DESCRIPTION

    keywords=['blog', 'informacion', 'increible', 'desarrollo web', 'desarrollo', 'website', 'develop', 'desarrollador']

    extra_props = {
	    'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
	   	}
    extra_custom_props=[
	    ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
	   	]

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title_page'] = "Contáctanos"
       	context['breadcrumb'] = [
           (reverse_lazy('home'), 'home'), ('', 'Contáctanos')
		]
		
        return context

def error_404(request, exception):
    data = {}
    return render(request, 'components/error_404.html', data)
