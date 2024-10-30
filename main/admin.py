from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import Comment, Course, Lesson, Category,\
                    UserProfile, Rating, Video, User, File


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']


class UserProfileInline(admin.TabularInline):
    model = UserProfile
    extra = 1


class CustomUserAdmin(DefaultUserAdmin):
    inlines = [UserProfileInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


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
