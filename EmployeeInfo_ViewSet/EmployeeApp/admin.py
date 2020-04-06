from django.contrib import admin
from EmployeeApp.models import Employee
# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display=['id','Emp_no','Emp_name','Emp_sal','Emp_addr']

admin.site.register(Employee,EmployeeAdmin)  