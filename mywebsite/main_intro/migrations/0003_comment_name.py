# Generated by Django 4.2.17 on 2025-01-05 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_intro', '0002_article_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
