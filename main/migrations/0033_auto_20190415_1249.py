# Generated by Django 2.1.7 on 2019-04-15 19:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_auto_20190415_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='article_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Articles', verbose_name='Article'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment_raw',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='parent_comment_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='profile_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Profiles', verbose_name='Profile'),
        ),
        migrations.AlterField(
            model_name='query_runs',
            name='query_runtime',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 15, 12, 49, 19, 334313), verbose_name='Query Runtime'),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_published',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 15, 12, 49, 19, 332313), verbose_name='date published'),
        ),
    ]
