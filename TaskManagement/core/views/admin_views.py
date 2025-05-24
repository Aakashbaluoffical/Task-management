from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from core.models.task_models import Task
from core.models.user_models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout

from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages



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
                return render(request, 'login.html', {'error': 'Access Denied'})  # fallback
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
    if request.user.role not in ['superadmin']:
        return redirect('login')
    
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role'] if request.user.role == 'superadmin' else 'user'
        if not User.objects.filter(username = request.POST['username']).exists():
            
            User.objects.create_user(
                username=username,
                is_active=True,
                password=password,
                role=role,
                is_staff=True if request.POST['role'] == 'admin' else False,
                is_superuser = False
            )
            messages.success(request, f"User '{request.POST['username']}' created successfully.")
        else:    
            messages.error(request, f"Username '{username}' already exists.")
    
    role = request.GET.get('role')
    user_list = User.objects.filter(is_active=True).exclude(id=request.user.id)
    if role:
        user_list = user_list.filter(role=role)
    
    paginator = Paginator(user_list, 5)
    page_number = request.GET.get('page')
    user_list = paginator.get_page(page_number)

    return render(request, 'superadmin/users.html', {'users': user_list})



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






# --- Admin Views ---
@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('login')
    return render(request, 'admin/dashboard.html')


# @login_required
# def admin_tasks(request):
#     if request.user.role != 'admin':
#         return redirect('login')
   
#     # Handle GET request (List + filter)
#     status = request.GET.get('status')
#     task_list = Task.objects.filter(is_active=True)
#     if status:
#         task_list = task_list.filter(status=status)

#     paginator = Paginator(task_list, 5)
#     page_number = request.GET.get('page')
#     tasks = paginator.get_page(page_number)

#     # For user dropdown
#     users = User.objects.filter(is_active=True).values('id', 'username')

#     return render(request, 'admin/task.html', {
#         'tasks': tasks,
#         'users': users
#     })


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
        
        user.delete()
    return redirect('superadmin_users')


def logout_view(request):
    logout(request)
    return redirect('login')




@login_required
@require_http_methods(["GET", "POST"])
def superadmin_tasks(request):
    if request.user.role not in ['superadmin','admin']:
        return redirect('login')

    # Handle POST request (Create task)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        assigned_to_id = request.POST.get('assigned_to')

        assigned_to_user = User.objects.filter(id=assigned_to_id, is_active=True).first()

        if assigned_to_user:
            Task.objects.create(
                title=title,
                description=description,
                due_date=due_date,
                assigned_to=assigned_to_user,
                status='pending',
                worked_hours=0,
                completion_report=None,
                is_active=True
            )
        if request.user.role == 'admin':
            return redirect('admin_tasks')
    
        return redirect('superadmin_tasks')  # Ensure this is the name in your urls.py

    # Handle GET request (List + filter)
    status = request.GET.get('status')
    task_list = Task.objects.filter(is_active=True)
    if status:
        task_list = task_list.filter(status=status)

    paginator = Paginator(task_list, 5)
    page_number = request.GET.get('page')
    tasks = paginator.get_page(page_number)

    # For user dropdown
    users = User.objects.filter(is_active=True).values('id', 'username')
    if request.user.role == 'admin':
        location = 'admin/task.html'
    else:
        location = 'superadmin/tasks.html'
    
    return render(request, location, {
        'tasks': tasks,
        'users': users
    })
    


@login_required
@require_http_methods(["GET", "POST"])
def edit_task(request, task_id):
    if request.user.role not in ['superadmin','admin']:
        return redirect('login')
   
    task = get_object_or_404(Task, id=task_id, is_active=True)
    
    if request.method == 'POST':
        title = request.POST.get('title', task.title)
        description = request.POST.get('description', task.description)
        due_date = request.POST.get('due_date', task.due_date)
        
        # Restrict admin users from modifying completion-related fields
        if request.user.role == 'admin':
            # Admin is not allowed to set status to 'completed' or edit completion data
            status = request.POST.get('status', task.status) if request.POST.get('status', task.status) != 'completed'  else task.status
               
            worked_hours = task.worked_hours
            completion_report = task.completion_report
        else:
            status = request.POST.get('status', task.status)
            worked_hours = request.POST.get('worked_hours', task.worked_hours)
            completion_report = request.POST.get('completion_report')

        errors = []

        if status == 'completed' and request.user.role != 'admin':
            if not worked_hours:
                errors.append("Worked hours is required when task is completed.")
            if not completion_report:
                errors.append("Completion report is required when task is completed.")

        if errors:
            users = User.objects.filter(is_active=True)
            return render(request, 'superadmin/edit_task.html', {
                'task': task,
                'users': users,
                'errors': errors,
                'form_data': request.POST,
                'status_options': ['pending', 'in_progress', 'completed']
            })

        task.title = title
        task.description = description
        task.due_date = due_date
        task.status = status
        task.worked_hours = worked_hours
        if status == 'completed' and request.user.role != 'admin':
            task.completion_report = completion_report

        assigned_to_id = request.POST.get('assigned_to')
        assigned_to_user = User.objects.filter(id=assigned_to_id, is_active=True).first()
        if assigned_to_user:
            task.assigned_to = assigned_to_user

        task.save()

        if request.user.role == 'admin':
            return redirect('admin_tasks')
        else:
            return redirect('superadmin_tasks')

    users = User.objects.filter(is_active=True)
    # return render(request, 'superadmin/edit_task.html', {'task': task, 'users': users})
    status_options = ['pending', 'in_progress', 'completed']
   
    # if request.user.role == 'admin':
    #     status_options = ['pending', 'in_progress',]

    return render(request, 'superadmin/edit_task.html', {
        'task': task,
        'users': users,
        'status_options': status_options,
    })


@login_required
@require_http_methods(["POST"])
def delete_task(request, task_id):
    if request.user.role != 'superadmin':
        return redirect('admin_tasks')
    
    task = get_object_or_404(Task, id=task_id, is_active=True)
    task.is_active = False
    task.save()
    return redirect('superadmin_tasks')
