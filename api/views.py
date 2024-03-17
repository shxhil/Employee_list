from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.viewsets import ViewSet

from crm.models import Employees

from api.serializers import EmployeeSerializer

from rest_framework import authentication,permissions

from rest_framework.decorators import action


class EmployeeListCreatView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Employees.objects.all()
        #deserialize
        serializer=EmployeeSerializer(qs,many=True)#many=true means one or more objects from models idukkan .all()

        return Response(data=serializer.data)
    
    def post(self,request,*args,**kwargs):
        #seialization
        serializer=EmployeeSerializer(data=request.data)#user send cheytha => data=request.data
        if serializer.is_valid():           #request.POST in forms
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
        return Response(data={"message":"creating employees"})



#localhost:8000/api/employee/{id}  
#method:get,put,delete   
class EmplyeeMixinView(APIView):
    
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employees.objects.get(id=id)
        #deserializer
        serializer=EmployeeSerializer(qs,many=False)
        # return Response(data={"message":"retvive specific employee"})
        return Response(data=serializer.data)
    
    def patch(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        empoloyee_obj=Employees.objects.get(id=id)
        serializer=EmployeeSerializer(data=request.data,instance=empoloyee_obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)  


    def delete(self,*args,**kwargs):
        id=kwargs.get("pk")
        Employees.objects.get(id=id).delete()
        return Response(data={"message":"delete employee"})
             
#_________________viewsetview____________
class EmployeeViewsetView(ViewSet):
   
   authentication_classes=[authentication.BasicAuthentication]
   permission_classes=[permissions.IsAuthenticated]

   def list(self,request,*args,**kwargs):
       qs=Employees.objects.all()
       if "department" in request.query_params:
           value=request.query_params.get("department")
           qs=qs.filter(department=value)
           print(qs)
       serializer=EmployeeSerializer(qs,many=True)
       

       return Response(data=serializer.data)
   
   def create(self,request,*args,**kwargs):
       #data send cheyyanindaavm 
       serializer=EmployeeSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(data=serializer.data)
       else:
           return Response(data=serializer.errors)
   #specific
   def retrieve(self,request,*args,**kwargs):
       id=kwargs.get("pk")
       qs=Employees.objects.get(id=id)
       serialize=EmployeeSerializer(qs)
       return Response(data=serialize.data)

   def update(self,request,*args,**kwargs):
       id=kwargs.get("pk")
       employee_object=Employees.objects.get(id=id) 
       serializer=EmployeeSerializer(data=request.data,instance=employee_object)
       if serializer.is_valid():
           serializer.save()
           return Response(data=serializer.data)
       else:
           return Response(data=serializer.errors)

   def destroy(self,request,*args,**kwargs):
       id=kwargs.get("pk")
       Employees.objects.get(id=id).delete()
       return Response(data={"message":"delete employee"})
    
    #url:localhost:8000/api/v2/employees/all_departments/
    #method:get
   @action(methods=["get"], detail=False) #url ll id illa so detail=false 
   def all_departments(self,request,*args,**kwargs):
    #unique,no repetition
       qs=Employees.objects.all().values_list("department",flat=True).distinct()
       return Response(data=qs)