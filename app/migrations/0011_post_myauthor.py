# Generated by Django 4.1.2 on 2022-10-20 00:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_post_author_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='myauthor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.profile'),
        ),
    ]