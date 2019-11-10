from .models import Post, Category, SubCategory, Tag
from django import forms
from django.utils.translation import ugettext_lazy as _
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django_select2.forms import Select2MultipleWidget,ModelSelect2TagWidget
from blog.forms import MyModelSelect2TagWidget
from .models import Course

class CourseForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['category'].required = True

	class Meta:
		model = Course
		fields = ['title', 
				'description', 
				'category', 
				'subcategory',
				'content',
				'image',
				'tags',
				'is_active',
				]

		widgets = {
			'title': forms.TextInput(attrs={'class':'form-control'}),
			'description': forms.TextInput(attrs={'class':'form-control'}),
			'category': forms.Select(attrs={'class':'form-control'}),
			'subcategory': forms.Select(attrs={'class':'form-control'}),
			'content': CKEditorUploadingWidget(),
			'tags': MyModelSelect2TagWidget(search_fields = [
			        'tag__icontains',
			    ],	
			    attrs={'class':'form-control'}),
			'is_active': forms.CheckboxInput()
        }

		labels = {
            "title": _("Titulo"),
            "description": _("Descripción"),
            "category": _("Categoría"),
            "subcategory": _("Subcategoría"),
            "content": _("Contenido"),
            "image": _("Imagen"),
            "tags": _("Tags"),
            "is_active": _("Mostrar Curso?")
        }

	def clean_category(self):
		data = self.cleaned_data['category']
		if data == None:
			raise forms.ValidationError("This field is required")

		return data

	def clean_subcategory(self):

		data = self.cleaned_data['subcategory']

		if data != None:
			try:
				data = SubCategory.objects.get(pk=data.pk)
				return data

			except TypeError:
				raise forms.ValidationError("Invalid field value")

			except SubCategory.DoesNotExist:
				raise forms.ValidationError("Invalid field")

		raise forms.ValidationError("This field is required")
