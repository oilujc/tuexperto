from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from rest_framework import routers
from .views import (SubscriberCreateView,)

app_name = 'api_accounts'
urlpatterns = [

	#Token
    path('token', obtain_jwt_token, name='obtain_jwt_token'),
    path('token/verify', verify_jwt_token, name='verify_jwt_token'),
    path('token/refresh/', refresh_jwt_token, name='refresh_jwt_token'),

    path('subscriber', SubscriberCreateView.as_view(), name='subscriber_create'),

]
