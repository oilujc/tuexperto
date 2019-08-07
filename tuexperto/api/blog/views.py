from .serializers import (CategorySerializer, SubCategorySerializer )
from blog.models import (Category, SubCategory,)
from django.http import Http404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import (ListAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView, DestroyAPIView)
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):

	serializer_class = CategorySerializer
	permission_classes = [AllowAny]
	lookup_field = 'slug'

	def get_queryset(self):
		return Category.objects.all()

class SubCategoryViewSet(mixins.ListModelMixin, GenericViewSet):

	serializer_class = SubCategorySerializer
	permission_classes = [AllowAny]

	def get_queryset(self):

		qs = SubCategory.objects.all()
		category = self.request.query_params.get('category', None)

		if category is not None:
			qs = qs.filter(category__pk=category)

		return qs