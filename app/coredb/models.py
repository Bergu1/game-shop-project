from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


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


class PersonGames(models.Model):
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey('Games', on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        verbose_name = 'person_game' 
        verbose_name_plural = 'person_games'


class AccountHistory(models.Model):
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey('Games', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'accounthistory' 
        verbose_name_plural = 'accounthistory'


class Friends(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_requests", on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="received_requests", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'friends' 
        verbose_name_plural = 'friends'