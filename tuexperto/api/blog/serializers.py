from rest_framework import serializers

from blog.models import (Category, SubCategory)


class CategorySerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Category
		fields = (
		 		'category',
		 		'slug',
		 		)


class SubCategorySerializer(serializers.ModelSerializer):

	category = serializers.SerializerMethodField()

	def get_category(self, obj):
		return CategorySerializer(obj.category).data
	
	class Meta:
		model = SubCategory
		fields = (
				'id',
		 		'category',
		 		'subcategory',
		 		'slug',
		 		)