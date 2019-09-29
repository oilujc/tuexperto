from rest_framework import status

from rest_framework.views import APIView
from rest_framework.generics import (ListAPIView,
									 CreateAPIView,
									 RetrieveAPIView,
									 UpdateAPIView,
									 DestroyAPIView)

from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.response import Response

from .serializers import SubscriberSerializer

from accounts.models import Subscriber
from blog.models import Post
from utils.email_send import email_send
from django.contrib.sites.shortcuts import get_current_site
from api.blog.serializers import PostSerializer

class SubscriberCreateView(APIView):
	permission_classes = [AllowAny]

	def post(self, request, format=None):
		serializer = SubscriberSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			current_site = get_current_site(request)
			posts = Post.objects.filter(post_type="pt").order_by('-created_at')[:5]
			context = {
				'companyName': 'TuExperto.pro',
				'posts': posts,
				'domain': current_site.domain,
			}

			to_email = [serializer.data["email"]]


			email_send("auth/email_newsletter_template.html" ,context ,"Nuevo Suscriptor" ,to_email )

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)