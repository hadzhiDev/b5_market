from rest_framework.permissions import BasePermission


class IsOwnerORSuperUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        owner = obj.owner
        if owner == request.user or request.user.is_superuser:
            return True
        
    def has_permission(self, request, view):
        return super().has_permission(request, view)
 