# Generated by Django 5.1.2 on 2024-10-23 16:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts_app.comment'),
        ),
    ]
