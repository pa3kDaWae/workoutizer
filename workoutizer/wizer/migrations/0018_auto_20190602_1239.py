# Generated by Django 2.2.1 on 2019-06-02 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wizer', '0017_auto_20190602_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='date',
            field=models.DateTimeField(),
        ),
    ]