# Generated by Django 5.1.2 on 2024-12-11 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicatie_exemplu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='test_field',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]