# Generated by Django 3.2 on 2021-07-31 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('later', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='salt',
            field=models.CharField(default=1, max_length=1023),
            preserve_default=False,
        ),
    ]
