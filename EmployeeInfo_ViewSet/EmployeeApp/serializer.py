from EmployeeApp.models import Employee
from rest_framework.serializers import ModelSerializer

class EmployeeSerializer(ModelSerializer):
    class Meta:
        model=Employee
        fields='__all__'