from django.shortcuts import render,redirect
from django.views.generic import View
from crm.forms import EmployeeModelForm,RegistrationForm,LoginForm
from django.contrib import messages
from crm.models import Employees
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout 
from django.utils.decorators import method_decorator

# Create your views here.



#decarator creation

def signin_required(fn):

    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
        
    return wrapper



  #decorator
@method_decorator(signin_required,name="dispatch")
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
        
            return render(request,"emp_add.html",{"form":form})

        else:
            messages.error(request,"failed to add")
            return render(request,"emp_add.html",{"form":form})
              
@method_decorator(signin_required,name="dispatch")
class EmployeeListView(View):
    def get(self,request,*args,**kwargs):
        qs=Employees.objects.all()
        departments=Employees.objects.all().values_list("department",flat=True).distinct()#unique
        print(departments)
        if "department" in request.GET:
            dept=request.GET.get("department")
            qs=qs.filter(department__iexact=dept)
        return render(request,"emp_list.html",{"data":qs,"departments":departments})
       
        
    def post(self,request,*args,**kwargs):
        name=request.POST.get("box")
        qs=Employees.objects.filter(name__icontains=name)
        return render(request,"emp_list.html",{"data":qs})

@method_decorator(signin_required,name="dispatch")
class EmployeeDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employees.objects.get(id=id)
        return render(request,"emp_details.html",{"data":qs})

@method_decorator(signin_required,name="dispatch")
class EmployeeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Employees.objects.get(id=id).delete()
        messages.success(request,"employee deleted  succesfully")
        return redirect("emp-list")

@method_decorator(signin_required,name="dispatch")
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
        

class SignupView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"registration.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            # form.save()
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"Account succesfully created")
            print("saved")
            return render(request,"registration.html",{"form":form})
        else:
            messages.error(request,"failed to creat account")
            print("failed")
            return render(request,"registration.html",{"form":form})

# class SigninView(View):
#     def get(self,request,*args,**kwargs):
#         form=LoginForm()
#         return render(request,"login.html",{"form":form})
    
#     def post(self,request,*args,**kwargs):
#         form=LoginForm(request.POST)
#         if form.is_valid():
#             user_name=form.cleaned_data.get("username")
#             pwd=form.cleaned_data.get("password")
#             print(user_name,pwd)
#             user_obj=authenticate(request,username=user_name,password=pwd)
#             if user_obj:
#                 print("valid credential")
#                 login(request,user_obj)
#                 messages.success(request,"valid credential")
#                 return redirect("emp-list")
#         else:
#             messages.error(request,"invalid credentail")
#             return render(request,"login.html",{"form":form})


      
            # else:
            #     print("invalid credential")
            #     messages.error(request,"invalid credentail")


            # return render(request,"login.html",{"form":form})
        # else:
        #      messages.error(request,"invalid credentail")
        #      return render(request,"login.html",{"form":form})

class SigninView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")
            user_obj = authenticate(request, username=user_name, password=pwd)
            print("user_obj:", user_obj)
            if user_obj:
                login(request, user_obj)
                messages.success(request, "Valid credentials")
                return redirect("emp-list")
            else:
                messages.error(request, "Invalid credentials")
                
        return render(request, "login.html", {"form": form})

@method_decorator(signin_required,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        messages.error(request,"logout")
        return redirect("signin")
           