from rest_framework.permissions import BasePermission

class IsOwnerofStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        if request.user == view.get_object().owner