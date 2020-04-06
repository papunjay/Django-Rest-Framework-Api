from django.contrib import admin
# Register your models here.
from EmployeeApp.models import Employee
class EmployeeAdmin(admin.ModelAdmin):
    list_display=['id','Emp_no','Emp_name','Emp_sal','Emp_addr']

admin.site.register(Employee,EmployeeAdmin)
