from django.urls import path

from . import views
from rest_framework.routers import SimpleRouter, DefaultRouter


routers = DefaultRouter()
routers.register('category', views.CategoryView)
routers.register('course', views.CourseView)
routers.register('lesson', views.LessonView)
routers.register('lesson/(?P<lesson_pk>\d+)/video', views.VideoView)
routers.register('lesson/(?P<lesson_pk>\d+)/file', views.FileView)
routers.register('lesson/(?P<lesson_pk>\d+)/comment', views.CommentView, basename="lesson-comments")
routers.register('lesson/(?P<lesson_pk>\d+)/rating', views.RatingView, basename="lesson-ratings")


app_name = 'main'
urlpatterns = routers.urls

urlpatterns.append( path('send-mail/', views.UpdateViewSet.as_view(), name="send-mail"))
