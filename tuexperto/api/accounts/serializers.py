from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import Subscriber

class UserSerializer(serializers.ModelSerializer):
	full_name = serializers.SerializerMethodField()

	def to_representation(self, obj):
		ret = super().to_representation(obj)

		if obj.is_superuser != True:
			ret.pop('is_superuser')

		if obj.is_superuser != True:
			ret.pop('is_staff')

		return ret
	
	class Meta:
		model = get_user_model()
		fields = ('username',
				'full_name',
				'is_superuser',
				'is_staff',
				)

	def get_full_name(self, obj):
		return obj.get_full_name()


class SubscriberSerializer(serializers.ModelSerializer):

	class Meta:
		model = Subscriber
		fields = ('email',
				)