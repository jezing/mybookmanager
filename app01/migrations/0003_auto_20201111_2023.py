# Generated by Django 3.1.3 on 2020-11-11 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_book'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='pbs_id',
            new_name='publisher',
        ),
    ]