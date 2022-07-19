from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('keyboards/', views.keyboards_index, name='index'),
    # path('contact/', views.contact, name='contact'),
]
