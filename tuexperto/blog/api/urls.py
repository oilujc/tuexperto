from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from rest_framework import routers

from .views import (CategoryViewSet, SubCategoryViewSet, PostViewSet)

router = routers.DefaultRouter()
router.register('category', CategoryViewSet, basename='api_category')
router.register('subcategory', SubCategoryViewSet, basename='api_subcategory')
router.register('post', PostViewSet, basename='api_post')


app_name = 'api_blog'
urlpatterns = [

]

urlpatterns += router.urls