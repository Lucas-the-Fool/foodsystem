# Generated by Django 4.0.5 on 2024-03-19 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info_manage', '0003_remove_foodmodel_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodmodel',
            name='number',
        ),
    ]
