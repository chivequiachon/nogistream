# Generated by Django 2.1.5 on 2019-04-18 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VideoManagement', '0002_videoinfo_is_disabled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoinfo',
            name='filetype',
        ),
        migrations.AddField(
            model_name='videoinfo',
            name='embed_link',
            field=models.CharField(default='Enter embed link here', max_length=350),
        ),
    ]
