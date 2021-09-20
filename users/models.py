import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import MinLengthValidator


class UserManager(BaseUserManager):
    '''
    creating a manager for a custom user model
    '''

    def create_user(self, username=None, password=None, role='B'):
        """
        Create and return a `User` with an username, password
        and extra field.
        """
        if username is None:
            raise ValueError('Users Must Have a Username')

        if password is None:
            raise ValueError('Users Must Have a Password')

        user = self.model(
            username=username,

        )
        user.role = role
        user.set_password(password)
        user.save(using=self._db)
        if user.role == 'B':
            dep = Deposit(buyerId=user)
            dep.save()
        return user

    def create_superuser(self, username=None, password=None, role='B'):
        """
        Create and return a `User` with superuser (admin) permissions.
        """

        if username is None:
            raise ValueError('Superusers Must Have a Username')

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, password, role)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        if user.role == 'B':
            dep = Deposit(buyerId=user)
            dep.save()
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(validators=[MinLengthValidator(5)], max_length=10, unique=True)
    ROLE_CHOICES = (
        ('B', 'Buyer'),
        ('S', 'Seller'),
    )
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "user"


class Deposit(models.Model):
    buyerId = models.ForeignKey(User, to_field="username", db_column="buyerId", on_delete=models.CASCADE)
    fives = models.PositiveIntegerField(default=0)
    tens = models.PositiveIntegerField(default=0)
    twenties = models.PositiveIntegerField(default=0)
    fifties = models.PositiveIntegerField(default=0)
    hundreds = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "deposit"