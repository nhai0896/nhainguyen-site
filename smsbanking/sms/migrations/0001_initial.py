# Generated by Django 2.1.1 on 2018-10-09 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_message', models.CharField(max_length=500)),
                ('bank', models.CharField(max_length=500)),
                ('tk', models.CharField(max_length=500)),
                ('time', models.CharField(max_length=500)),
                ('amount', models.CharField(max_length=500)),
                ('currency', models.CharField(max_length=500)),
                ('content', models.CharField(max_length=500)),
                ('service', models.CharField(max_length=500)),
            ],
        ),
    ]