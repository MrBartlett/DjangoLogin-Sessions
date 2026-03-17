from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('LoggedInOnly/', views.logged_in_only, name='logged_in_only'),
    path("logout/", views.logout_view, name="logout"),
]

