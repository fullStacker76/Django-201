from django.urls import path, re_path
from . import views

from allauth.account import views as all_auth_views

app_name = "profiles"

urlpatterns = [
    path("<str:username>/",views.ProfileDetailView.as_view(),name="detail"),
    path("<int:pk>/edit/", views.ProfileUpdateView.as_view(),name="edit"),
    path("<int:pk>/delete/", views.ProfileDeleteView.as_view(),name="delete"),
    path("<str:username>/follow/",views.FollowerView.as_view(),name="follow"),        
]
