from django.shortcuts import render
from django.views.generic import View
import io
from rest_framework.parsers import JSONParser
from EmployeeApp.serializers import EmployeeSerializers
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from EmployeeApp.models import Employee
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt,name='dispatch')
class EmployeeCRUDCBV(View):
    def get(self,request,*args,**kwargs):
    # the line number 14,15,16,are use to convert json_file to pyhton native data [dic] ie. dserializers concept    
        json_data=request.body
        stream=io.BytesIO(json_data)
        python_data=JSONParser().parse(stream)
        id=python_data.get('id',None) #this line check this id is valid or not if not valid return None
        if id is not None:
            emp=Employee.objects.get(id=id) #this line emp holde models object of id 
            serializer=EmployeeSerializers(emp) #this line conver model object to pyhton dic
            json_data=JSONRenderer().render(serializer.data)
            return HttpResponse(json_data,content_type='appliction/json')
        #this line if id is not found the return the all value
        qs=Employee.objects.all()
        serializer=EmployeeSerializers(qs,many=True)
        return HttpResponse(json_data,content_type ='appliction/json')

    def post(self,request,*args,**kwargs):
        json_data=request.body #take the request of json data from third party
        #line number 35,36 convert json file to pyhton file 
        stream=io.BytesIO(json_data) 
        python_data=JSONParser().parse(stream)
        serializer=EmployeeSerializers(data=python_data) # this line conver pyhton file to database  suported file, all three line is dserialization
        if serializer.is_valid():
            serializer.save() # after this code create the data in database
            msg={'msg':'Resource Created Successfully'}
            json_data=JSONRenderer().render(msg)
            return HttpResponse(json_data,content_type ='appliction/json')
        json_data=JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type ='appliction/json',status=400)

    def put(self,request,*args,**kwargs):
        json_data=request.body
        stream=io.BytesIO(json_data)
        python_data=JSONParser().parse(stream)
        id=python_data.get('id')
        emp=Employee.objects.get(id=id)
        serializer=EmployeeSerializers(emp,data=python_data) #this line update full data 
        serializer=EmployeeSerializers(emp,data=python_data,partial=True) # this line update paritial data
        if serializer.is_valid():
            serializer.save()
            msg={'msg':'Resource Update Successfully'}
            json_data=JSONRenderer().render(msg)
            return HttpResponse(json_data,content_type ='appliction/json')
        json_data=JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type ='appliction/json',status=400)
        
    def delete(self,request):
        json_data=request.body
        stream=io.BytesIO(json_data)
        python_data=JSONParser().parse(stream)
        id=python_data.get('id')
        emp=Employee.objects.get(id=id)
        emp.delete()
        msg={'msg':'Resource Deleted Successfully'}
        json_data=JSONRenderer().render(msg)
        return HttpResponse(json_data,content_type='application/json')
