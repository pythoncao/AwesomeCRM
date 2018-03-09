from django.shortcuts import render,redirect,HttpResponse
from  django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from  django.db.models import Q
from django import conf
import json
from django.contrib.auth.decorators import login_required
import importlib
from cocoadmin import app_setup
from cocoadmin import form_handle

app_setup.cocoadmin_auto_discover()
from  cocoadmin.sites import site



# Create your views here.



def acc_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect(request.GET.get('next','/cocoadmin'))
    return render(request,'cocoadmin/login.html')

def acc_logout(request):
    logout(request)
    return redirect('/login')

def app_index(request):
    # enabled_admins =

    return render(request,'cocoadmin/app_index.html',{'site':site})

def get_orderby_result(request,querysets,admin_class):

    current_ordered_coloum = {}
    order_by = request.GET.get('_o')
    if order_by:
        orderby_key = admin_class.list_display[abs(int(order_by))]
        current_ordered_coloum[orderby_key] = order_by

        if order_by.startswith('-'):
            orderby_key = '-' + orderby_key
            print(order_by)
        return querysets.order_by(orderby_key),current_ordered_coloum
    else:
        return querysets,current_ordered_coloum

def get_filter_result(request,querysets):
    filter_conditions = {}
    for key,val in request.GET.items():
        if key in ("page","_o","_q"):
            continue
        if val:
            filter_conditions[key] = val

    return querysets.filter(**filter_conditions), filter_conditions

def get_searched_searched_result(request,querysets,admin_class):
    search_key = request.GET.get('_q')
    if search_key:
        q = Q()
        q.connector = 'OR'
        for search_field in admin_class.search_fields:
            q.children.append(("%s__contains"%search_field,search_key))

        return querysets.filter(q)
    return querysets





@login_required()
def table_obj_list(request, app_name, model_name):
    """取出指定model里数据返回"""
    admin_class = site.enabled_admins[app_name][model_name]
    if request.method =="POST":
        selected_action = request.POST.get('action')
        selected_ids = json.loads(request.POST.get('selected_ids'))
        if not selected_action:
            if selected_ids:
                admin_class.model.objects.filter(id__in=selected_ids).delete()
        else:
            selected_objs = admin_class.model.objects.filter(id__in=selected_ids)
            admin_action_func = getattr(admin_class,selected_action)
            response = admin_action_func(request,selected_objs)
            if response:
                return response


    querysets = admin_class.model.objects.all().order_by('-id')

    querysets,filter_conditions = get_filter_result(request,querysets)
    admin_class.filter_conditions = filter_conditions
    querysets = get_searched_searched_result(request,querysets,admin_class)
    admin_class.search_key = request.GET.get('_q','')

    querysets,sorted_coloum = get_orderby_result(request,querysets,admin_class)

    paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page

    page = request.GET.get('page')
    querysets = paginator.get_page(page)
    # print('------------------------------------------',sorted_coloum.values())

    return render(request, 'cocoadmin/table_obj_list.html', locals())


@login_required
def table_obj_change(request,app_name,model_name,obj_id):
    """数据修改"""
    admin_class = site.enabled_admins[app_name][model_name]
    model_form = form_handle.create_dynamic_model_form(admin_class)
    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == "GET":
        form_obj = model_form(instance=obj)
    elif request.method == "POST":
        form_obj = model_form(instance=obj, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/cocoadmin/%s/%s"%(app_name, model_name))
    return render(request, 'cocoadmin/table_obj_change.html', locals())

def table_obj_add(request, app_name, model_name):
    admin_class = site.enabled_admins[app_name][model_name]
    model_form = form_handle.create_dynamic_model_form(admin_class, form_add=True)
    if request.method == "GET":
        form_obj = model_form()

    elif request.method =='POST':
        form_obj = model_form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/cocoadmin/%s/%s" % (app_name, model_name))
    return render(request, 'cocoadmin/table_obj_add.html', locals())


@login_required
def table_obj_delete(request,app_name,model_name,obj_id):

    admin_class = site.enabled_admins[app_name][model_name]

    obj = admin_class.model.objects.get(id=obj_id)
    if request.method =="POST":
        obj.delete()
        return redirect("/cocoadmin/{app_name}/{model_name}".format(app_name=app_name,model_name=model_name))
    return render(request,'cocoadmin/table_obj_delete.html',locals())

