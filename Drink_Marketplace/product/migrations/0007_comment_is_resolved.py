# Generated by Django 5.1.7 on 2025-05-14 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_comment_needs_support'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_resolved',
            field=models.BooleanField(default=False),
        ),
    ]
