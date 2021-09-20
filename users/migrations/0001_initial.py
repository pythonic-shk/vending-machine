# Generated by Django 3.2.7 on 2021-09-16 16:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=10, unique=True, validators=[django.core.validators.MinLengthValidator(5)])),
                ('role', models.CharField(choices=[('B', 'Buyer'), ('S', 'Seller')], max_length=1)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fives', models.PositiveIntegerField(default=0)),
                ('tens', models.PositiveIntegerField(default=0)),
                ('twenties', models.PositiveIntegerField(default=0)),
                ('fifties', models.PositiveIntegerField(default=0)),
                ('hundreds', models.PositiveIntegerField(default=0)),
                ('total', models.PositiveIntegerField(default=0)),
                ('buyerId', models.ForeignKey(db_column='buyerId', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'db_table': 'deposit',
            },
        ),
    ]
