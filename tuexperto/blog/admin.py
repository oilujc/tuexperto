from .models import (Category, Tag, Post, SubCategory)
from ckeditor.widgets import (CKEditorWidget,)
from django import forms
from django.contrib import admin


# Register your models here.

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm



admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)





