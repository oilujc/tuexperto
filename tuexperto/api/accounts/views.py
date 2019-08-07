from rest_framework import status

from rest_framework.views import APIView
from rest_framework.generics import (ListAPIView,
									 CreateAPIView,
									 RetrieveAPIView,
									 UpdateAPIView,
									 DestroyAPIView)

from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.response import Response
