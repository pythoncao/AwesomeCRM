from django.shortcuts import render,redirect
from  django.contrib.auth import authenticate,login,logout


# Create your views here.
def acc_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect(request.GET.get('next','/crm'))
    return render(request,'login.html')

def acc_logout(request):
    logout(request)
    return redirect('/login')