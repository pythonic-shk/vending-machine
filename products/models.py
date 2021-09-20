import uuid
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sellerId = models.ForeignKey(User, to_field="username", db_column="sellerId", on_delete=models.CASCADE)
    amountAvailable = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    productName = models.CharField(max_length=50, unique=False, null=False, blank=False)
    cost = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "product"
        unique_together = ('productName', 'sellerId')
