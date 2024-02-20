from django.urls import path
from django.urls import re_path as url

from . import views

urlpatterns = [
    path("role/", views.RoleView.as_view(), name='get_create_roles'),
    path("role/<int:pk>/", views.SingleRoleView.as_view(), name='get_put_delete_role'), 
    path("user/", views.UserView.as_view(), name='get_user'), 
    path("signup/", views.SignUpView.as_view(), name='create_user'), 
    path("user/<int:pk>/", views.SingleUserView.as_view(), name='get_put_delete_user'), 
]