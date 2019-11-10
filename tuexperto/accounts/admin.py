from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (User,
                    Skill,
                    Subscriber,
                    UserEducation,
                    UserExperience,
                    MySite,
					)



# Register your models here.
class CustomUserAdmin(UserAdmin):
	fieldsets = UserAdmin.fieldsets + (
            ('Extra Fields', {
            'fields': (
            	'public_id',
                'image',
                'title',
                'country',
                'description',
                'short_description',
                'skills',
            	),
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Skill)
admin.site.register(Subscriber)
admin.site.register(UserEducation)
admin.site.register(UserExperience)
admin.site.register(MySite)
