# Generated by Django 3.2 on 2022-04-05 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('later', '0003_user_reading_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='finished',
            field=models.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='user',
            name='reading_list',
            field=models.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.CharField(max_length=300)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='later.user')),
            ],
        ),
    ]
