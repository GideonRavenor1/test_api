# Generated by Django 4.1.5 on 2023-01-21 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teasers', '0002_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='category',
            name='index_category_title',
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('title',), name='unique_category'),
        ),
    ]
