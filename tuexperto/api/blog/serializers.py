from rest_framework import serializers

from blog.models import (Category, SubCategory, Post)


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


class PostSerializer(serializers.ModelSerializer):

	category = serializers.SerializerMethodField()
	subcategory = serializers.SerializerMethodField()


	def get_category(self, obj):
		return CategorySerializer(obj.category).data

	def get_category(self, obj):
		return SubCategorySerializer(obj.subcategory).data
	
	class Meta:
		model = Post
		fields = (
				'description',
		 		'category',
		 		'subcategory',
		 		'title',
		 		'slug',
		 		'content',
		 		'image',
		 		'created_at',
		 		'post_type',
		 		'tags',
		 		'is_active',
		 		)