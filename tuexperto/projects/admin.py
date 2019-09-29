from django.contrib import admin
from .models import Project, Team
from ckeditor.widgets import (CKEditorWidget,)
from django import forms

# Register your models here.

class ProjectAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Project
        fields = '__all__'

class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm

admin.site.register(Project, ProjectAdmin)
admin.site.register(Team)