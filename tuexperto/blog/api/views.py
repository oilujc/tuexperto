from .serializers import (CategorySerializer, SubCategorySerializer, PostSerializer)
from blog.models import (Category, SubCategory, Post)
from django.http import Http404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import (ListAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView, DestroyAPIView)
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework import mixins
from rest_framework import authentication, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class CategoryViewSet(ReadOnlyModelViewSet):

	serializer_class = CategorySerializer
	lookup_field = 'slug'

	def get_queryset(self):
		return Category.objects.all()

class SubCategoryViewSet(ReadOnlyModelViewSet):

	serializer_class = SubCategorySerializer

	def get_queryset(self):

		qs = SubCategory.objects.all()
		category = self.request.query_params.get('category', None)

		if category is not None:
			qs = qs.filter(category__pk=category)

		return qs

class PostViewSet(ReadOnlyModelViewSet):

	authentication_classes = [TokenAuthentication, JSONWebTokenAuthentication]
	serializer_class = PostSerializer
	lookup_field = 'slug'

	def get_queryset(self):
		return Post.objects.filter(is_active=True, post_type='pt')