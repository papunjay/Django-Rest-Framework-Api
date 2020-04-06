from django.db import models

class Employee(models.Model):
    Emp_no=models.IntegerField()
    Emp_name=models.CharField(max_length=64)
    Emp_sal=models.FloatField()
    Emp_addr=models.CharField(max_length=64)


    