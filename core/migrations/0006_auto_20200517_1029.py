# Generated by Django 3.0.6 on 2020-05-17 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200517_1027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productuploadmodel',
            old_name='processed_rows',
            new_name='imported_rows',
        ),
    ]
