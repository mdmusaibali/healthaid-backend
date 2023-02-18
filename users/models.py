from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import random
import string

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

   

    def create_superuser(self, email, password, name):
        user = self.create_user(email=email, password=password, name=name, is_superuser = True)
        user.is_superadmin = True
        user.is_staff = True
        user.is_patient = False
        user.save(using=self._db)
        return user

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_patient = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

class Patient(models.Model):
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    patient_id = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    phone_number = models.CharField(max_length=15)
    aadhar_number = models.CharField(max_length=12)
    picture = models.ImageField(upload_to='patient_pictures/', null = True)
    
    def save(self, *args, **kwargs):
        if not self.patient_id:
            self.patient_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        super(Patient, self).save(*args, **kwargs)

    def __str__(self):
         return self.name


class Staff(models.Model):
    user = models.OneToOneField(User, related_name = "Staff", on_delete=models.CASCADE, primary_key=True)
# returning staff name
    def __str__(self):
         return self.user.name
