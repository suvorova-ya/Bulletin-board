# Generated by Django 4.0.6 on 2022-09-09 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(null=True, verbose_name='URLcom'),
        ),
    ]