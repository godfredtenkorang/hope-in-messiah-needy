# Generated by Django 4.1 on 2023-04-13 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foundation', '0011_alter_galary_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='galary',
            name='title',
        ),
    ]
