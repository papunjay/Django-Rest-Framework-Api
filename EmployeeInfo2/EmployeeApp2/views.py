from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from EmployeeApp2.serializer import NameSerializer
from rest_framework.viewsets import ViewSet
# class TestAPIView(APIView):
#     def get(self,request,*args,**kwargs):
#         colors=['Red','yellow','Green','Blue']
#         return Response({'msg':'happy pongal','colors':colors})# this code convert python dic data to json data 

#     def post(self,request,*args,**kwargs):
#         serializer=NameSerializer(data=request.data)
#         if serializer.is_valid():
#             name=serializer.data.get('name')
#             msg='Hello {},happy pongal !!!'.format(name)
#             return Response({'msg':msg})
#         else:
#             return Response(serializer.error,status=400)

class TestViewSet(ViewSet):
    def list(self,request):
        colors=['RED','YELLOW','GREEN','BLUE']
        return Response({'msg':'Happy new year','color':colors})
    
    def create(self,request):
        serializer=NameSerializer(data=request.data)
        if serializer.is_valid():
            name=serializer.data.get('name')
            msg='Hello {} Happy pongal !!!'.format(name)
            return Response({'msg':msg})
        else:
            return Response(serializer.errors,status=400)
