from rest_framework.permissions import BasePermission

class IsOwnerOrStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user == view.get_object().owner

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.owner == request.user


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff == False:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff == False:
            return obj.owner == request.user
        return True


class CustomCoursePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'PUT', 'PATCH'] and request.user.is_staff:    # Разрешить только изменение (PUT, PATCH) для модераторов
            return True
        if request.user.is_authenticated and not request.user.is_staff:    # Разрешить все операции для аутентифицированных пользователей
            return True
        return False