from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from functools import wraps

# Create your views here.
def index(request):
    
    return render(request, 'index.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)

        if user is not None:
            if user.is_staff:
                login(request,user)
                request.session['is_admin_logged_in'] = True
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'You are not authorized to access admin panel.')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'admin/admin_login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


#Custom Decorator for Admin Panel Access
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            messages.error(request, "You must login as admin to access this page.")
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def admin_dashboard(request):

    return render(request,'admin/admin_dashboard.html')