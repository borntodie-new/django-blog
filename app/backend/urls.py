from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('get_code_image/', views.get_code_image, name='get_code_image')
]
