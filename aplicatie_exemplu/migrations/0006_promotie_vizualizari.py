# Generated by Django 5.1.2 on 2024-12-17 17:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicatie_exemplu', '0005_customuser_cod_customuser_email_confirmat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=100)),
                ('data_creare', models.DateTimeField(auto_now_add=True)),
                ('data_expirare', models.DateTimeField()),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('mesaj_personalizat', models.TextField()),
                ('meniu', models.ManyToManyField(related_name='promotii', to='aplicatie_exemplu.meniu')),
            ],
        ),
        migrations.CreateModel(
            name='Vizualizari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_vizualizare', models.DateTimeField(auto_now_add=True)),
                ('produs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicatie_exemplu.pizza')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-data_vizualizare'],
            },
        ),
    ]
