from django.urls import path
#from pages import views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("home/", views.home, name='home'),
    path("portfolio/", views.portfolio, name='portfolio'),
    path("watchlist/", views.watchlist, name='watchlist'),
    path("notifications/", views.notifications, name='notifications'),
]
