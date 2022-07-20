from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('keyboards/', views.keyboards_index, name='index'),
    path('keyboard/<int:keyboard_id>/', views.keyboards_detail, name='detail'),
    path('keyboards/create/', views.KeyboardCreate.as_view(), name='keyboards_create'),
    path('keyboards/<int:pk>/update/', views.KeyboardUpdate.as_view(), name='keyboards_update'),
    path('keyboards/<int:pk>/delete/', views.KeyboardDelete.as_view(), name='keyboards_delete'),
    path('keyboards/<int:keyboard_id>/add_cleaning/', views.add_cleaning, name='add_cleaning'),
    path('keyboards/<int:keyboard_id>/add_photo/', views.add_photo, name='add_photo'),
    
    path('keyboards/<int:keyboard_id>/associated_part/<int:part_id>/', views.associate_part, name='associate_part'),
    
    path('parts/', views.PartList.as_view(), name='parts_index'),
    path('parts/<int:pk>/', views.PartDetail.as_view(), name='parts_detail'),
    path('parts/create/', views.PartCreate.as_view(), name='parts_create'),
    path('parts/<int:pk>/update/', views.PartUpdate.as_view(), name='parts_update'),
    path('parts/<int:pk>/delete/', views.PartDelete.as_view(), name='parts_delete'),
]
