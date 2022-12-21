# Generated by Django 4.1.4 on 2022-12-12 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('command', models.TextField()),
                ('status', models.CharField(choices=[('new', 'New'), ('running', 'Running'), ('done', 'Done'), ('stopped', 'Stopped')], default='new', max_length=100)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]