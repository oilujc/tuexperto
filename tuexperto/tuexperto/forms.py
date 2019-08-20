from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_select2.forms import Select2MultipleWidget

class SignupForm(UserCreationForm):

	password1 = forms.CharField(label='Password',
				widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
	password2 = forms.CharField(label='Confirm Password',
				widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))

	terms = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))

	class Meta:

		model = get_user_model()
		fields = (
			'username',
			'first_name', 
			'last_name', 
			'email',
			'country',
			'password1',
			'password2',
			)
		widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':"Username"}),
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':"First name"}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':"Last name"}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':"Email address"}),
            'country': forms.Select(attrs={'class':'form-control', 'placeholder':"Country"}), 
				 }


	def clean_password2(self):

		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")

		if password1 != password2:
			raise forms.ValidationError("Passwords must match")

	def clean_email(self):

		email = self.cleaned_data.get("email")
		user = get_user_model()
		try:
			user = user.objects.get(email=email)
		except user.DoesNotExist:
			return email

		raise forms.ValidationError("The email entered already exists")


	def clean_password(self):

		password = self.cleaned_data.get("password1")
		
		if len(password) < 8:
			raise forms.ValidationError("The password must be at least 8 characters")

# class EditForm(UserChangeForm):

# 	class Meta:

# 		model = get_user_model()
# 		fields = (
# 			'first_name', 
# 			'last_name', 
# 			'image',
# 			'user_body',
# 			'address',
# 			)
# 		widgets = {
#             'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}),
#             'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}),
#             'address': forms.TextInput(attrs={'class':'form-control'}),
#      		'image' : forms.FileInput(attrs={'class':'form-control'}),

#         }