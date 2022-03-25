from operator import mod
from django.db import models

# Create your models here.


class Employee(models.Model):
    name = models.CharField(max_length=255)

class FileGroup(models.Model):
    name = models.CharField(max_length=255)
    employee = models.ForeignKey("Employee",related_name = "filess", on_delete=models.CASCADE)