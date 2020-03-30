# Generated by Django 3.0.4 on 2020-03-30 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_suggestedgift'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permalink',
            fields=[
                ('key', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('refers_to', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Recipient')),
            ],
        ),
    ]
