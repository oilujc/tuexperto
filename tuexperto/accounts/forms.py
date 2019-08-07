from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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