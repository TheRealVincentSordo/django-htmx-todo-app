from django.urls import path
from . import views

app_name = "todos"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("", views.index, name="index"),
    path("add/", views.add_todo, name="add"),
    path("<int:todo_id>/toggle/", views.toggle_todo, name="toggle"),
    path("<int:todo_id>/delete/", views.delete_todo, name="delete"),
]
