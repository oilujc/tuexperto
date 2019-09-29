from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from meta.models import ModelMeta
from utils.generators import (unique_slug_generator,unique_categories_slug_generator)
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

from blog.models import (Category, SubCategory, Tag)

# Create your models here.
def project_directory_path(instance, filename):
	filename = "{0}".format(slugify(instance.title))
	return '{0}/{1}'.format(slugify(instance.title),filename)


class Project(ModelMeta, models.Model):

	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

	title = models.CharField(max_length=150, unique=True)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=150, blank=True, null=True)
	content = RichTextUploadingField()

	url = models.URLField()

	image = models.ImageField(upload_to=project_directory_path)

	show_project = models.BooleanField(default=False)

	check_in = models.DateField()
	check_out = models.DateField()

	status = models.CharField(max_length=2, choices=(('st', 'Started'), ('dv', 'Development'), ('pr', 'Production')),default='st')

	tags = models.ManyToManyField(Tag)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

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
		verbose_name = "Project"
		verbose_name_plural = "Projects"

	def __str__(self):
		return self.title



class Team(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Team"
		verbose_name_plural = "Teams"
	
	def __str__(self):
		pass

@receiver(post_save, sender=Project)
def post_save_project(sender, instance,created, **kwargs):
	if not instance.slug:
		instance.slug = "{0}".format(unique_slug_generator(instance))
		instance.save()