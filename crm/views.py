from django.shortcuts import render
from django.views.generic import View
from crm.forms import EmplyeeForm
from crm.models import Employees
# Create your views here.

class EmployeeCreateView(View):
    def get (self,request,*args,**kwargs):
        form=EmplyeeForm()
        return render(request,"emp_add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=EmplyeeForm(request.POST)
        if form.is_valid():
            Employees.objects.create(**form.cleaned_data)
            print("created")
            return render(request,"emp_add.html",{"form":form})
        else:
            return render(request,"emp_add.html",{"form":form})
              