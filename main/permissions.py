from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaff(BasePermission):
    message = "Faqat xodimlar uchun."
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff
