from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from meta.models import ModelMeta
from utils.generators import (
    unique_slug_generator, unique_categories_slug_generator)
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

from django.utils.encoding import python_2_unicode_compatible
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation

from blog.models import (Post, Category, SubCategory, Tag)

def course_directory_path(instance, filename):
    filename = "{0}.jpg".format(slugify(instance.title))
    return '{0}/{1}'.format(slugify(instance.title), filename)

class Course(ModelMeta, models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    description = models.CharField(max_length=200)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE)

    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    content = RichTextUploadingField()

    image = models.ImageField(upload_to=course_directory_path)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(Tag)

    posts = models.ManyToManyField(Post, blank=True)

    is_active = models.BooleanField(default=True)

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
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.title

@receiver(post_save, sender=Course)
def course_save_post(sender, instance, created, **kwargs):
    if not instance.slug:
        instance.slug = "{0}".format(unique_slug_generator(instance))
        instance.save()
