from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('profile/', views.ProfileView.as_view(), name='my_profile'),
=======
>>>>>>> 72f4066fa5748c0921f8bba8fa79ee453233c999
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/roles/', views.UserRoleUpdateView.as_view(), name='user_roles'),
    path('roles/create/', views.GroupCreateView.as_view(), name='group_create'),
]