import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models.task_models import Task
from datetime import date, timedelta

User = get_user_model()

@pytest.fixture
def superadmin_user(db):
    return User.objects.create_user(username='superadmin', password='superpass', role='superadmin', is_active=True, is_staff=True)

@pytest.fixture
def admin_user(db):
    return User.objects.create_user(username='admin', password='adminpass', role='admin', is_active=True, is_staff=True)

@pytest.fixture
def client_login(client, superadmin_user):
    client.login(username='superadmin', password='superpass')
    return client

@pytest.fixture
def task(admin_user):
    return Task.objects.create(
        title='Test Task',
        description='Test Description',
        due_date=date.today() + timedelta(days=7),
        assigned_to=admin_user,
        status='pending',
        worked_hours=0,
        is_active=True
    )


# --- Landing page
def test_landing_view(client):
    response = client.get(reverse('landing_view'))
    assert response.status_code == 200


# --- Login Tests

def test_login_valid(client, superadmin_user):
    response = client.post(reverse('login'), {'username': 'superadmin', 'password': 'superpass'})
    assert response.status_code == 302  # redirect after login
@pytest.mark.django_db
def test_login_invalid(client):
    response = client.post(reverse('login'), {'username': 'wrong', 'password': 'wrong'})
    assert b'Invalid credentials' in response.content


# --- Superadmin Dashboard
def test_superadmin_dashboard(client_login):
    response = client_login.get(reverse('superadmin_dashboard'))
    assert response.status_code == 200


# --- User Creation
def test_create_user_view(client_login):
    response = client_login.post(reverse('superadmin_users'), {
        'username': 'newuser',
        'password': 'testpass',
        'role': 'admin'
    })
    assert User.objects.filter(username='newuser').exists()


# --- Duplicate User Creation
def test_create_duplicate_user(client_login, superadmin_user):
    response = client_login.post(reverse('superadmin_users'), {
        'username': 'superadmin',
        'password': 'testpass',
        'role': 'admin'
    })
    assert b"already exists" in response.content


# --- Edit User
def test_edit_user(client_login, admin_user):
    response = client_login.post(reverse('edit_user', args=[admin_user.id]), {
        'username': 'updatedadmin',
        'role': 'admin'
    })
    updated_user = User.objects.get(id=admin_user.id)
    assert updated_user.username == 'updatedadmin'


# --- Delete User
def test_delete_user(client_login, admin_user):
    response = client_login.post(reverse('delete_user', args=[admin_user.id]))
    assert not User.objects.filter(id=admin_user.id).exists()


# --- Create Task
def test_create_task(client_login, admin_user):
    response = client_login.post(reverse('superadmin_tasks'), {
        'title': 'New Task',
        'description': 'Task description',
        'due_date': str(date.today() + timedelta(days=2)),
        'assigned_to': admin_user.id
    })
    assert Task.objects.filter(title='New Task').exists()


# --- Edit Task
def test_edit_task(client_login, task, admin_user):
    response = client_login.post(reverse('edit_task', args=[task.id]), {
        'title': 'Updated Task',
        'description': 'Updated Desc',
        'due_date': str(date.today() + timedelta(days=5)),
        'status': 'in_progress',
        'assigned_to': admin_user.id
    })
    task.refresh_from_db()
    assert task.title == 'Updated Task'
    assert task.status == 'in_progress'


# --- Delete Task
def test_delete_task(client_login, task):
    response = client_login.post(reverse('delete_task', args=[task.id]))
    task.refresh_from_db()
    assert task.is_active is False


# --- Unauthorized Access
def test_admin_cannot_access_superadmin_views(client, admin_user):
    client.login(username='admin', password='adminpass')
    response = client.get(reverse('superadmin_users'))
    assert response.status_code == 302  # Redirect to login due to access restriction
