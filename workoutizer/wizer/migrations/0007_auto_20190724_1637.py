# Generated by Django 2.2.1 on 2019-07-24 16:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wizer', '0006_auto_20190724_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]