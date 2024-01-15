from django.urls import path
from api import views

from rest_framework.routers import DefaultRouter
#defaultRouter nta akatha register function call,inherit akaan ahn object aayt router
router=DefaultRouter()
                #(prefix/viewset/basename)
router.register("v2/employees",views.EmployeeViewsetView,basename="employees")
                            #/vechend cheyyard already
# for u in router.urls:
#     print("++",u,"+++")

urlpatterns=[
    path("employees/",views.EmployeeListCreatView.as_view()),
    path("employees/<int:pk>/",views.EmplyeeMixinView.as_view()),

]+router.urls

#locathost:8000/api/v2/employees/
#method:get => list

#localhost:8000/api/v2/employees/
#method:post => create

#localhost:8000/api/v2/employees/(id)/
#method:get =>retrive

#localhost:8000/api/v2/employees/(id)/
#method:put =>update

#locathost:800/api/v2/employes/(id)/
#method:delete =>destroy
