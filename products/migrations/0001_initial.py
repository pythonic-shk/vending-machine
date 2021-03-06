# Generated by Django 3.2.7 on 2021-09-16 16:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amountAvailable', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('productName', models.CharField(max_length=50)),
                ('cost', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('sellerId', models.ForeignKey(db_column='sellerId', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'db_table': 'product',
                'unique_together': {('productName', 'sellerId')},
            },
        ),
    ]
