# Generated by Django 5.1.2 on 2024-12-11 01:52

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ambalaj',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=20, unique=True)),
                ('material', models.CharField(choices=[('plastic', 'Plastic'), ('carton', 'Carton')], default='carton', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='AmbalajPrajitura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=20, unique=True)),
                ('material', models.CharField(choices=[('plastic', 'Plastic'), ('hartie', 'Hartie'), ('carton', 'Carton')], max_length=10)),
                ('pret', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=100, unique=True)),
                ('calorii', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='IngredientPrajitura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=30, unique=True)),
                ('calorii', models.IntegerField()),
                ('unitate', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Locatie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresa', models.CharField(max_length=255)),
                ('oras', models.CharField(max_length=100)),
                ('judet', models.CharField(max_length=100)),
                ('cod_postal', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Meniu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=50, unique=True)),
                ('descriere', models.TextField(blank=True, null=True)),
                ('data_creare', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organizator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('telefon', models.CharField(blank=True, max_length=15)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Eveniment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_eveniment', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('titlu', models.CharField(max_length=200)),
                ('descriere', models.TextField()),
                ('tip_eveniment', models.CharField(choices=[('conferinta', 'Conferinta'), ('workshop', 'Workshop'), ('intalnire', 'Intalnire'), ('webinar', 'Webinar')], max_length=50)),
                ('capacitate', models.PositiveIntegerField()),
                ('este_public', models.BooleanField(default=True)),
                ('imagine', models.ImageField(blank=True, null=True, upload_to='imagini_evenimente/')),
                ('website', models.URLField(blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('data_creare', models.DateTimeField(auto_now_add=True)),
                ('data_actualizare', models.DateTimeField(auto_now=True)),
                ('locatie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='aplicatie_exemplu.locatie')),
                ('organizator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evenimente', to='aplicatie_exemplu.organizator')),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=100, unique=True)),
                ('descriere', models.TextField(blank=True, null=True)),
                ('pret', models.DecimalField(decimal_places=2, max_digits=6)),
                ('gramaj', models.PositiveIntegerField()),
                ('ambalaj', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aplicatie_exemplu.ambalaj')),
                ('ingrediente', models.ManyToManyField(to='aplicatie_exemplu.ingredient')),
                ('meniu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicatie_exemplu.meniu')),
            ],
        ),
        migrations.CreateModel(
            name='Comanda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_comanda', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('nume_client', models.CharField(max_length=100)),
                ('data_comanda', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('pizzas', models.ManyToManyField(to='aplicatie_exemplu.pizza')),
            ],
        ),
        migrations.CreateModel(
            name='Prajitura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=20, unique=True)),
                ('descriere', models.TextField(null=True)),
                ('pret', models.DecimalField(decimal_places=2, max_digits=8)),
                ('gramaj', models.PositiveBigIntegerField()),
                ('temperatura', models.IntegerField()),
                ('tip_produs', models.CharField(choices=[('cofetarie', 'Cofetarie'), ('patiserie', 'Patiserie'), ('gelaterie', 'Gelaterie')], default='cofetarie', max_length=50, null=True)),
                ('calorii', models.IntegerField()),
                ('categorie', models.CharField(choices=[('comanda speciala', 'Comanda speciala'), ('aniversara', 'Aniversara'), ('editie limitata', 'Editie limitata'), ('pentru copii', 'Pentru copii'), ('dietetica', 'Dietetica'), ('comuna', 'Comuna')], default='comuna', max_length=50, null=True)),
                ('pt_diabetici', models.BooleanField(default=False)),
                ('imagine', models.ImageField(blank=True, null=True, upload_to='imagini_prajituri/')),
                ('data_adaugare', models.DateTimeField(auto_now_add=True, null=True)),
                ('ambalaj', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aplicatie_exemplu.ambalaj')),
                ('ingrediente', models.ManyToManyField(to='aplicatie_exemplu.ingredient')),
            ],
        ),
    ]
