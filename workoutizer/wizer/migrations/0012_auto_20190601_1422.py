# Generated by Django 2.2.1 on 2019-06-01 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wizer', '0011_auto_20190601_1420'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sport',
            old_name='name_slug',
            new_name='slug',
        ),
    ]