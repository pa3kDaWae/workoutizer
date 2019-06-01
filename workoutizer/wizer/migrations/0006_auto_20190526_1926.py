# Generated by Django 2.2.1 on 2019-05-26 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wizer', '0005_auto_20190526_1646'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sport',
            old_name='sport',
            new_name='sports_name',
        ),
        migrations.AddField(
            model_name='sport',
            name='icon',
            field=models.CharField(default='none', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sport',
            name='color',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]