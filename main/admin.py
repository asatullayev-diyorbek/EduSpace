from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Comment, Course, Lesson, Category, \
    Rating, Video, File, User, Update


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'first_name', 'last_name', 'role', 'is_staff', 'is_active', 'get_profile_image']
    list_display_links = ['pk', 'username',]

    def get_profile_image(self, obj):
        return mark_safe(f'<img src="{obj.get_image()}" alt="No image" style="width:75px; height=75px; border-radius:50%" />')
    get_profile_image.short_description = 'Picture'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'created_by', 'created_at', 'updated_at', 'is_active']
    list_display_links = ['id', 'name']


class VideoInline(admin.TabularInline):
    model = Video
    extra = 1


class FileInline(admin.TabularInline):
    model = File
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['user', 'content', 'lesson', 'created_at']


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0
    readonly_fields = ['user', 'lesson', 'liked']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'title', 'created_at', 'updated_at']
    list_display_links = ['id', 'course']
    inlines = [VideoInline, FileInline, CommentInline, RatingInline]


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'created_at']
