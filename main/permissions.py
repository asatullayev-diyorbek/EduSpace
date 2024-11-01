from rest_framework.permissions import BasePermission
from .models import ADMIN, STUDENT, Course, Lesson


class IsAuthor(BasePermission):
    message = "Ushbu amalni bajarishga ruxsatingiz yo'q."

    def has_permission(self, request, view):
        # Umumiy ruxsatni tekshiradi
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        elif request.method == 'POST':
            # Faqatgina ADMIN foydalanuvchilar POST qilishi mumkin
            return request.user.is_authenticated and request.user.role == ADMIN
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Aniq obyekt uchun ruxsatni tekshiradi
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated and request.user.role == ADMIN
        else:
            # obj Course ekanini tekshiradi va muallifligini tasdiqlaydi
            if isinstance(obj, Course):
                return obj.created_by == request.user
            if isinstance(obj, Lesson):
                return obj.course.created_by == request.user
            return request.user.role == ADMIN


class IsStudent(BasePermission):
    message = "Ushbu amalni bajarishga ruxsatingiz yo'q."
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_authenticated and request.user.role == STUDENT


class IsAdmin(BasePermission):
    message = "Ushbu amalni bajarishga ruxsatingiz yo'q."
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_authenticated and request.user.role == ADMIN
