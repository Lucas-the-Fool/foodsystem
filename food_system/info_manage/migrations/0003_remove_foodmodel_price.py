# Generated by Django 4.0.5 on 2024-03-19 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info_manage', '0002_remove_userinfomodel_money_alter_foodmodel_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodmodel',
            name='price',
        ),
    ]
