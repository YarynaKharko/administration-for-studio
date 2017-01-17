# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-17 17:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20170117_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortfolioImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portfolio_image', models.ImageField(upload_to=b'')),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='project_main_image',
            field=models.ImageField(upload_to=b''),
        ),
        migrations.AddField(
            model_name='project',
            name='portfolio',
            field=models.ManyToManyField(to='projects.PortfolioImage'),
        ),
    ]
