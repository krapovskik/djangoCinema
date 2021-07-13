from django.urls import path
from . import views

app_name = 'cinema'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register', views.UserRegisterFormView.as_view(), name='register'),
    path('login', views.UserLoginFormView.as_view(), name='login'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('movies', views.MovieView.as_view(), name='movie'),
    path('movies/movie_name', views.MovieNameView.as_view(), name='movie_name'),
    path('movies/movie_price', views.MoviePriceView.as_view(), name='movie_price'),
    path('details/<int:pk>', views.MovieDetailView.as_view(), name='movie_details'),
    path('addMovie', views.MovieCreateView.as_view(), name='add_movie'),
    path('order/<int:pk>', views.movieOrder, name='order'),
    path('delete/<int:pk>', views.MovieDeleteView.as_view(), name='delete'),
    path('edit/<int:pk>', views.MovieUpdateView.as_view(), name='edit'),
]
