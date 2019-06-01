# Generated by Django 2.2.1 on 2019-05-26 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sport', models.CharField(max_length=200)),
                ('color', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date published')),
                ('duration', models.DateTimeField(blank=True)),
                ('distance', models.IntegerField()),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wizer.Sport')),
            ],
        ),
    ]