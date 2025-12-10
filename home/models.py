from django.db import models

class Conta(models.Model):
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)

# Create your models here.
