from rest_framework.permissions import BasePermission 
from core.models.user_models import User
from core.models.task_models import Task



class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin' and request.user.is_active)

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and  request.user.role == 'superadmin'and request.user.is_active)

class IsAdminOrSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated  and
            request.user.role in ['admin', 'superadmin'] and request.user.is_active
        )

class IsUser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and 
            request.user.role == 'user' and request.user.is_active
        )