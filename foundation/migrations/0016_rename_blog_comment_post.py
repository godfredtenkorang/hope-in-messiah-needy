# Generated by Django 4.1 on 2023-04-29 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foundation', '0015_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='blog',
            new_name='post',
        ),
    ]