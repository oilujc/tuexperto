# Generated by Django 2.2.3 on 2019-07-10 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_show_in_navbar'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
