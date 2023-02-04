from rest_framework import permissions

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_patient

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superadmin
