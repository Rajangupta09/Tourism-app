# Generated by Django 2.2.15 on 2020-12-25 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0007_auto_20201225_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='approve',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.TextField()),
                ('read', models.BooleanField(default=False)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signup.Contact')),
            ],
        ),
    ]
