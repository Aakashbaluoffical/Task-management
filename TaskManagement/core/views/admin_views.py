from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from core.models.task_models import Task
from core.models.user_models import User
from django.shortcuts import render, redirect, get_object_or_404


class AdminPanal(APIView):
    def get(self, request):
        return Response({"message": "This is the admin panel"})


# --- Login View ---
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            if user.role == 'superadmin':
                return redirect('superadmin_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('login')  # fallback
        return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def landing_view(request):
    
    return render(request, 'index.html')


# --- SuperAdmin Views ---
@login_required
def superadmin_dashboard(request):
    if request.user.role != 'superadmin':
        return redirect('login')
    return render(request, 'superadmin/dashboard.html')


@login_required
def superadmin_users(request):
    if request.user.role != 'superadmin':
        return redirect('login')
    users = User.objects.filter(is_active=True)
    return render(request, 'superadmin/users.html', {'users': users})

@login_required
def superadmin_users(request):
    if request.user.role not in ['superadmin', 'admin']:
        return redirect('login')

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role'] if request.user.role == 'superadmin' else 'user'
        
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            created_by=request.user
        )

    users = User.objects.filter(is_active=True).exclude(id=request.user.id)
    return render(request, 'superadmin/users.html', {'users': users})



@login_required
def superadmin_roles(request):
    if request.user.role != 'superadmin':
        return redirect('login')
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        role = request.POST.get('role')
        try:
            user = User.objects.get(id=user_id, is_active=True)
            user.role = role
            user.save()
        except User.DoesNotExist:
            pass
    users = User.objects.filter(is_active=True)
    return render(request, 'superadmin/roles.html', {'users': users})


@login_required
def superadmin_tasks(request):
    if request.user.role != 'superadmin':
        return redirect('login')
    tasks = Task.objects.filter(is_active=True)
    return render(request, 'superadmin/tasks.html', {'tasks': tasks})


# --- Admin Views ---
@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('login')
    return render(request, 'admin/dashboard.html')


@login_required
def admin_tasks(request):
    if request.user.role != 'admin':
        return redirect('login')
    tasks = Task.objects.filter(assigned_to=request.user, is_active=True)
    return render(request, 'admin/tasks.html', {'tasks': tasks})


# --- Task Report View ---
@login_required
def task_report_detail(request, task_id):
    task = Task.objects.filter(id=task_id, is_active=True, status='completed').first()
    if not task:
        return render(request, '404.html')  # custom 404 page
    return render(request, 'reports/task_detail.html', {'task': task})


@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST['username']
        user.role = request.POST['role']
        user.save()
        return redirect('superadmin_users')
    return render(request, 'edit_user.html', {'user': user})


@login_required
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_active = False
        user.save()
    return redirect('superadmin_users')





