# Generated by Django 3.2.5 on 2023-04-09 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='domain',
            field=models.CharField(max_length=20, null=True),
        ),
    ]