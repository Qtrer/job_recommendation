from django.urls import path
from django.contrib import admin
from django.conf.urls import url
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index),
    path('employee/<int:id>', views.employeeIndex, name='employeeIndex'),
]