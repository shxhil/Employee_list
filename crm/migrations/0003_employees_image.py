# Generated by Django 3.2.22 on 2023-11-08 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_rename_emploees_employees'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]