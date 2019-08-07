from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from meta.models import ModelMeta
from utils.generators import (unique_slug_generator,unique_categories_slug_generator)
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

from django.utils.encoding import python_2_unicode_compatible
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation

def post_directory_path(instance, filename):
	filename = "{0}.jpg".format(slugify(instance.title))
	return '{0}/{1}'.format(slugify(instance.title),filename)

class Category(ModelMeta, models.Model):

	category = models.CharField(max_length=50)

	description = models.CharField(max_length=200, blank=True, null=True)

	slug = models.SlugField(blank=True, null=True)

	_metadata = {
		'title': 'title',
		'description': 'description',
		'extra_props': 'extra_props',
		'extra_custom_props': 'custom_props'
		}
	
	created_at = models.DateTimeField(auto_now_add=True)

	@property
	def title(self):
		return self.category.title()

	def extra_props(self):
		return {'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'}

	def custom_props(self):
		return [('http-equiv', 'Content-Type', 'text/html; charset=UTF-8')]

	class Meta:
		verbose_name = "Category"
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.category

class SubCategory(ModelMeta, models.Model):

	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	subcategory = models.CharField(max_length=50)

	description = models.CharField(max_length=200, blank=True, null=True)

	slug = models.SlugField(blank=True, null=True)

	_metadata = {
		'title': 'title',
		'description': 'description',
		'extra_props': 'extra_props',
		'extra_custom_props': 'custom_props'
		}
	
	created_at = models.DateTimeField(auto_now_add=True)

	@property
	def title(self):
		return self.subcategory.title()
	

	def extra_props(self):
		return {'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'}

	def custom_props(self):
		return [('http-equiv', 'Content-Type', 'text/html; charset=UTF-8')]

	class Meta:
		verbose_name = "Subcategory"
		verbose_name_plural = "Subcategories"

	def __str__(self):
		return self.title

class Tag(models.Model):

	tag = models.CharField(max_length=50, unique=True)

	class Meta:
		verbose_name = "Tag"
		verbose_name_plural = "Tags"

	def __str__(self):
		return self.tag
   
class Post(ModelMeta, models.Model):
	
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

	description = models.CharField(max_length=200)

	category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
	subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)

	title = models.CharField(max_length=150, unique=True)
	slug = models.SlugField(unique=True,blank=True, null=True)

	content = RichTextUploadingField()

	image = models.ImageField(upload_to=post_directory_path)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	post_type = models.CharField(max_length=2, choices=(('pg', 'page'), ('pt', 'post')),default='pt')

	tags = models.ManyToManyField(Tag)

	is_active = models.BooleanField(default=True)

	show_in_navbar = models.BooleanField(default=False)

	_metadata = {
		'title': 'title',
		'description': 'description',
		'keywords': 'get_kw',
		'extra_props': 'extra_props',
		'extra_custom_props': 'custom_props'
		}


	def get_kw(self):
		tags = self.tags.all()
		if tags.count() > 0:
			return [x.tag for x in tags]

		return []

	def extra_props(self):
		return {'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'}

	def custom_props(self):
		return [('http-equiv', 'Content-Type', 'text/html; charset=UTF-8')]

	class Meta:
		verbose_name = "Post"
		verbose_name_plural = "Posts"

	def __str__(self):
		return self.title

@receiver(post_save, sender=Category)
def post_save_categories(sender, instance,created, **kwargs):
	if not instance.slug:
		instance.slug = "{0}".format(unique_slug_generator(instance))
		instance.save()

@receiver(post_save, sender=SubCategory)
def post_save_subcategories(sender, instance,created, **kwargs):
	if not instance.slug:
		instance.slug = "{0}".format(unique_slug_generator(instance))
		instance.save()

@receiver(post_save, sender=Post)
def post_save_post(sender, instance,created, **kwargs):
	if not instance.slug:
		instance.slug = "{0}".format(unique_slug_generator(instance))
		instance.save()