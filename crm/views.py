from django.shortcuts import render
from django.views.generic import View
from crm.forms import EmplyeeForm,EmployeeModelForm

from crm.models import Employees
# Create your views here.

class EmployeeCreateView(View):
    def get (self,request,*args,**kwargs):
        form=EmployeeModelForm()
        return render(request,"emp_add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=EmployeeModelForm(request.POST)
        if form.is_valid():
            form.save()
            # Employees.objects.create(**form.cleaned_data)
            print("created")
            return render(request,"emp_add.html",{"form":form})
        else:
            return render(request,"emp_add.html",{"form":form})
              

class EmployeeListView(View):
    def get(self,request,*args,**kwargs):
        qs=Employees.objects.all()
        return render(request,"emp_list.html",{"data":qs})