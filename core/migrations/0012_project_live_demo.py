# Generated by Django 5.2 on 2025-04-19 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_project_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='live_demo',
            field=models.URLField(blank=True, null=True),
        ),
    ]
