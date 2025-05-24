from django.urls import path
from core.views.admin_views import AdminPanal
from core.views.data_insertion_views import insert_data
from core.views import admin_views

urlpatterns = [
    # Optional custom admin panel (commented out)
    # path('admin/', AdminPanal.as_view(), name='custom_admin'),

    # Upload route for data insertion
    path('upload/<str:table_name>/', insert_data, name='file_upload'),

    path('', admin_views.landing_view, name='login'),

    # Login page
    path('login', admin_views.login_view, name='login'),

    # SuperAdmin URLs
    path('superadmin/dashboard/', admin_views.superadmin_dashboard, name='superadmin_dashboard'),
    path('superadmin/users/', admin_views.superadmin_users, name='superadmin_users'),
    path('superadmin/roles/', admin_views.superadmin_roles, name='superadmin_roles'),
    path('superadmin/tasks/', admin_views.superadmin_tasks, name='superadmin_tasks'),

    path('superadmin/edit/<int:user_id>/', admin_views.edit_user, name='edit_user'),
    path('superadmin/delete/<int:user_id>/', admin_views.delete_user, name='delete_user'),






    # Admin URLs
    path('admin/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin/tasks/', admin_views.admin_tasks, name='admin_tasks'),

    # Task Report Detail
    path('task/<int:task_id>/report/', admin_views.task_report_detail, name='task_report_detail'),
]
