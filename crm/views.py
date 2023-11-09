from django.shortcuts import render,redirect
from django.views.generic import View
from crm.forms import EmployeeModelForm
from django.contrib import messages
from crm.models import Employees
# Create your views here.

class EmployeeCreateView(View):
    def get (self,request,*args,**kwargs):
        form=EmployeeModelForm()
        return render(request,"emp_add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=EmployeeModelForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"employee added succesfully")
            # Employees.objects.create(**form.cleaned_data)
            print("created")
        
            return redirect("")

        else:
            messages.error(request,"failed to add")
            return render(request,"emp_add.html",{"form":form})
              

class EmployeeListView(View):
    def get(self,request,*args,**kwargs):
        qs=Employees.objects.all()
        return render(request,"emp_list.html",{"data":qs})
    
    def post(self,request,*args,**kwargs):
        name=request.POST.get("box")
        qs=Employees.objects.filter(name_icontains=name)
        return render(request,"emp_list.html",{"data":qs})

class EmployeeDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employees.objects.get(id=id)
        return render(request,"emp_details.html",{"data":qs})
    
class EmployeeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Employees.objects.get(id=id).delete()
        messages.success(request,"employee deleted  succesfully")
        return redirect("emp-list")
    
class EmployeeUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Employees.objects.get(id=id)
        form=EmployeeModelForm(instance=obj)
        return render(request,"emp_edit.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Employees.objects.get(id=id)
        form=EmployeeModelForm(request.POST, instance=obj,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"updated succesfully")

            # return redirect("emp-detils", pk=id)
            return redirect("emp-list")

        else:
            messages.error(request,"failed to update")
            return render(request,"emp_edit.html",{"form":form})