from django.urls import path
from . import views

app_name = "feed"

urlpatterns = [
    path("", views.HomePage.as_view(), name = "index"),
    path("<int:pk>/details/", views.PostDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.PostUpdateView.as_view(), name="edit"),
     path("<int:pk>/delete/", views.PostDeleteView.as_view(), name="delete"),
    path("new/", views.CreateNewPost.as_view(), name="new_post"),
]
