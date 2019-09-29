from django.db import models
from django.contrib.auth.models import AbstractUser
from meta.models import ModelMeta
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from utils.generators import random_string_generator,unique_countries_slug_generator
from ckeditor.fields import RichTextField
from utils.validators import validate_file_doc_extension
import datetime

def year_choices():
    return tuple([(r,r) for r in range(1984, datetime.date.today().year+1)])

def current_year():
    return datetime.date.today().year

def user_directory_path(instance, filename):
	filename = "{0}.jpg".format(instance.public_id)
	return '{0}/{1}'.format(instance.public_id,filename)

def user_filename_path(instance, filename):
	return '{0}/{1}'.format(instance.public_id,filename) 

class Skill(models.Model):

	skill = models.CharField(max_length=50, unique=True)

	class Meta:
		verbose_name = "Skill"
		verbose_name_plural = "Skills"

	def __str__(self):
		return self.skill
 
class Subscriber(models.Model):
	
	email = models.EmailField(unique=True)
	send_msg = models.BooleanField(default=True)

	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.email

	class Meta:
		verbose_name_plural = "Subscribers"


# Create your models here.
class User(ModelMeta, AbstractUser):

	_metadata = {
		'title': 'get_user_name',
		'description': 'short_description',
		'keywords': 'get_kw',
		'extra_props': 'extra_props',
		'extra_custom_props': 'custom_props'
		}

	public_id = models.SlugField(unique=True, blank=True, null=True)
	image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
	title = models.CharField(max_length=50, blank=True, null=True)
	short_description = models.CharField(max_length=150, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	send_email = models.BooleanField(default=True)
	user_type = models.CharField(max_length=2, choices=(('bs', 'Basic'), ('bl', 'Blogger')),default='bs')
	skills = models.ManyToManyField(Skill, blank=True)
	cv = models.FileField(upload_to=user_filename_path, blank=True, null=True,validators=[validate_file_doc_extension])
	country = CountryField(blank=True,null=True)
	contact_me = models.BooleanField(default=False)


	def extra_props(self):
		return {'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'}

	def custom_props(self):
		return [('http-equiv', 'Content-Type', 'text/html; charset=UTF-8')]

	@property
	def get_user_name(self):
		return self.username
	
	def get_kw(self):
		tags = self.skills.all()
		if tags.count() > 0:
			return [x.skill for x in tags]

		return []

	class Meta:
		verbose_name_plural = "Users"

class UserEducation(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	year_join = models.IntegerField(choices=year_choices(), default=current_year)
	year_finish = models.IntegerField(choices=year_choices(), default=current_year)
	title = models.CharField(max_length=150)
	description = models.CharField(max_length=200, blank=True, null=True)

class UserExperience(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=150)
	url = models.URLField()
	year_join = models.IntegerField(choices=year_choices(), default=current_year)
	year_finish = models.IntegerField(choices=year_choices(), default=current_year)
	description = models.CharField(max_length=200, blank=True, null=True)

@receiver(post_save, sender=User)
def post_save_user(sender, instance,created, **kwargs):
	if not instance.public_id:
		instance.public_id = "{0}".format(random_string_generator(size=10))
		instance.save()
