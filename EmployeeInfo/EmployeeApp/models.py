from django.db import models
# Create your models here.
class Employee(models.Model):
    Emp_no=models.IntegerField()
    Emp_name=models.CharField(max_length=20)
    Emp_sal=models.FloatField()
    Emp_addr=models.CharField(max_length=20)
