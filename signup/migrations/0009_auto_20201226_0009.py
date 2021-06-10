# Generated by Django 2.2.15 on 2020-12-25 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('signup', '0008_auto_20201225_2025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='email',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='name',
        ),
        migrations.AddField(
            model_name='tour',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
