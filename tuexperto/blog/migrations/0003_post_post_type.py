# Generated by Django 2.2.3 on 2019-07-10 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('pg', 'pg'), ('pt', 'pt')], default='pg', max_length=2),
        ),
    ]
