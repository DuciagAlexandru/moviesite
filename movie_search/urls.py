from django.urls import path
from movie_search import views

app_name = "movie_search"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("user_login/", views.user_login, name="user_login"),
    path("input_genre/", views.input_genre, name="input_genre"),
    path("search_result/", views.search_result, name="search_result"),
]
