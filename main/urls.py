from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter

routers = SimpleRouter()
routers.register('category', views.CategoryView)


app_name = 'main'
urlpatterns = routers.urls
