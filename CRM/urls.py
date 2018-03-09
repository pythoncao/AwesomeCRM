from django.urls import path,include,re_path
from  CRM import views

urlpatterns = [
    path('', views.dashboard,name="sales_dashboard"),
    path('stu_enrollment/', views.stu_enrollment, name="stu_enrollment"),
    re_path('^enrollment/(\d+)/$', views.enrollment, name="enrollment"),
    re_path('^enrollment/(\d+)/fileupload/$', views.enrollment_fileupload, name="enrollment_fileupload"),

]
