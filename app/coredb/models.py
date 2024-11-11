from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class PersonManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        person = self.model(username=username,
                    email=self.normalize_email(email),
                    **extra_fields)
        
        person.set_password(password)
        person.save(using=self._db)

        return person

    def create_superuser(self, username, email, password=None, **extra_fields):
        person = self.create_user(username, email, password, **extra_fields)
        person.is_staff = True
        person.is_superuser = True
        person.save(using=self._db)
        return person


class Person(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    total_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    currency = models.CharField(max_length=3, default='PLN')


    objects = PersonManager()

    class Meta:
        verbose_name = 'Person' 
        verbose_name_plural = 'Persons'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class Games(models.Model):
    id = models.BigAutoField(primary_key=True)
    tittle = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='games/')

    class Meta:
        verbose_name = 'Game' 
        verbose_name_plural = 'Games'