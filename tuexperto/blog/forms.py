from .models import Post, Category, SubCategory, Tag
from django import forms
from django.utils.translation import ugettext_lazy as _
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django_select2.forms import Select2MultipleWidget,ModelSelect2TagWidget


class MyModelSelect2TagWidget(ModelSelect2TagWidget):
	queryset = Tag.objects.all()

	def value_from_datadict(self, data, files, name):
		values = super().value_from_datadict(data, files, name)
		print(values)
		cleaned_values = []
		for val in values:
			try:
				obj, created = self.queryset.get_or_create(pk=int(val))
			except ValueError:
				obj, created = self.queryset.get_or_create(tag=str(val))

			cleaned_values.append(obj.pk)
		return cleaned_values

class PostForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['category'].required = True

	class Meta:
		model = Post
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
            "is_active": _("Mostrar entrada?")
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

class PageForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['title', 
				'description',
				'content',
				'image',
				'tags',
				'is_active',
				'show_in_navbar'
				]

		widgets = {
			'title': forms.TextInput(attrs={'class':'form-control'}),
			'description': forms.TextInput(attrs={'class':'form-control'}),
			'content': CKEditorUploadingWidget(),
			'tags': MyModelSelect2TagWidget(attrs={'class':'form-control'}),
			'is_active': forms.CheckboxInput(),
			'show_in_navbar': forms.CheckboxInput(),

        }

		labels = {
            "title": _("Titulo"),
            "description": _("Descripción"),
            "content": _("Contenido"),
            "image": _("Imagen"),
            "tags": _("Tags"),
            "is_active": _("Mostrar pagina?"),
            "show_in_navbar": _("Mostrar en el navbar?")
        }

