from rest_framework import serializers
from EmployeeApp.models import Employee
def multipal_value(value): # 1st priority of validation
    print('validation by validator')
    if value%1000 !=0: 
        raise serializers.ValidationError('Employee Salary should be multipale of 1000')
        return value
# # the line number 9,10,11,12 are responsible for do the create and update         
# class EmployeeSerializers(serializers.ModelSerializer):
#     class Meta:
#         model=Employee
#         fields='__all__'

####### this is simpale serializers ######## 
class EmployeeSerializers(serializers.Serializer):
    Emp_no=serializers.IntegerField()
    Emp_name=serializers.CharField()
    Emp_sal=serializers.FloatField(validators=[multipal_value])
    Emp_addr=serializers.CharField()
######### field validation 
    def validate_Emp_sal(self, value): #2Nd priority of validation
        print('field level validation')
        if value <5000:
            raise serializers.ValidationError('Employee Salary should v minimum 5000')
        return value

    def validate(self, data): #3rd priority of validation
        print('object level validation')
        Emp_name=data.get('Emp_name')
        Emp_sal=data.get('Emp_sal')
        if Emp_name.lower()=='shreya':
            if Emp_sal<50000:
                raise serializers.ValidationError('Employee Salary should v minimum 5000')
        raise serializers.ValidationError('this user not found in your database')
        return data



#the line number 9,10 create the data in database according to post request after the data is valid or not
    def create(self,validate_data):
        return Employee.objects.create(**validate_data)

    def update(self, instance, validated_data):# heare validataed data take the value from third party aplication
        instance.Emp_no=validated_data.get('Emp_no',instance.Emp_no) #heare instance.Emp_no is use for if third party not send the data we use existing data
        instance.Emp_name=validated_data.get('Emp_name',instance.Emp_name)
        instance.Emp_sal=validated_data.get('Emp_sal',instance.Emp_sal)
        instance.Emp_addr=validated_data.get('Emp_addr',instance.Emp_addr)
        instance.save()
        return instance
