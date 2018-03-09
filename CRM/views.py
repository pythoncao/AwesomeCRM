from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from CRM import models,forms
from django import conf
import os
@login_required()
def dashboard(request):
    return render(request,'crm/dashboard.html')

@login_required()
def stu_enrollment(request):

    customers = models.CustomerInfo.objects.all()
    class_lists = models.ClassList.objects.all()
    if request.method =="POST":
        customer_id = request.POST.get("customer_id")
        print('-------------------',customer_id)
        class_grade_id = request.POST.get("class_grade_id")
        enrollment_obj = models.StudentEnrollment.objects.create(
            customer_id =customer_id,
            class_grade_id = class_grade_id,
            consultant_id = request.user.userprofile.id,
        )
        enrollment_link = "http://localhost:8000/crm/enrollment/%s" %enrollment_obj.id


    return render(request,'crm/stu_enrollment.html',locals())



def enrollment(request,enrollment_id):
    """在线报名表"""

    enrollment_obj = models.StudentEnrollment.objects.get(id=enrollment_id)
    if request.method =="POST":

        customer_form = forms.CustomerForm(instance=enrollment_obj.customer,data=request.POST)
        if customer_form.is_valid():

            customer_form.save()
            return HttpResponse("提交成功")
    else:
        customer_form = forms.CustomerForm(instance=enrollment_obj.customer)
    return render(request,"crm/enrollment.html",locals())

@csrf_exempt
def enrollment_fileupload(request,enrollment_id):
    print(request.FILES)

    return HttpResponse('dddd')