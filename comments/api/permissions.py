from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return obj.user == request.user
        return True

    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.is_authenticated
        return True