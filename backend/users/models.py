from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, email, phone, name, password, role='user'):
        if not email:
            raise ValueError("Email is required")
        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            name=name,
            role=role
        )
        user.password = make_password(password)  # Hash the password
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)  # Hashed password
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'name', 'role']

class Disaster(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    precautions = models.TextField()

    def __str__(self):
        return self.name
    
class City(models.Model):
    cityName = models.CharField(max_length=255)
    subcity = models.CharField(max_length=255)
    route = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)
    services = models.CharField(max_length=255)

    def __str__(self):
        return self.cityName
    
class Disasterchatbot(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    causes = models.TextField()
    precautions = models.TextField()
    reference_link = models.URLField()

    def __str__(self):
        return self.name    
    
class Review(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    rating = models.IntegerField()
    review = models.TextField()

    def __str__(self):
        return self.name