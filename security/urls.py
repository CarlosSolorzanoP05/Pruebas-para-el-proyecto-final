from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/roles/', views.UserRoleUpdateView.as_view(), name='user_roles'),
]