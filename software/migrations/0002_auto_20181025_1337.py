# Generated by Django 2.1.2 on 2018-10-25 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('software', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='softwareproject',
            name='categories',
            field=models.ManyToManyField(to='software.Category'),
        ),
        migrations.AddField(
            model_name='softwareproject',
            name='technologies',
            field=models.ManyToManyField(to='software.TechUsed'),
        ),
    ]
