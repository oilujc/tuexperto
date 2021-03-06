# Generated by Django 2.2.3 on 2019-08-05 21:36

import accounts.models
from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_user_cv'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='contact_me',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='cv',
            field=models.FileField(blank=True, null=True, upload_to=accounts.models.user_filename_path, validators=[utils.validators.validate_file_doc_extension]),
        ),
    ]
