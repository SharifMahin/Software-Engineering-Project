# Generated by Django 3.1 on 2020-09-11 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_auto_20200911_2143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comment_count',
        ),
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(to='posts.Category'),
        ),
    ]