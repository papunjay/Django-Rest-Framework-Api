from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from EmployeeApp.models import Employee
from EmployeeApp.serializer import EmployeeSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class EmployeeCRUDCBV(ModelViewSet):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer


