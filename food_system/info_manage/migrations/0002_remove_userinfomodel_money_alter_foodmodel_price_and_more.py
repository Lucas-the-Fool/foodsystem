# Generated by Django 4.2.5 on 2024-03-19 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info_manage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfomodel',
            name='money',
        ),
        migrations.AlterField(
            model_name='foodmodel',
            name='price',
            field=models.IntegerField(default=0, verbose_name='价格'),
        ),
        migrations.DeleteModel(
            name='OrderModel',
        ),
    ]