from django.urls import path
#from pages import views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("home/", views.home, name='home'),
    path("portfolio/", views.portfolio, name='portfolio'),
    path("watchlist/", views.watchlist, name='watchlist'),
    path("notifications/", views.notifications, name='notifications'),
    path("search-results/", views.stock_search, name='stock_search'),
    path("details/", views.project_index, name="project_index"),
    path('new/', views.newProject, name='NewGroup'),
    path('EditItem/<int:product_id>/', views.newProject, name='NewGroup'),
    path("list/", views.project_list, name="project_list"),
    path('Game/', views.handle_game_details_request, name='Game'),
    path('newStudent/', views.CUStudent, name='NewStudent'),
    path('DeleteItem/<int:product_id>/', views.handle_delete_item_request, name='Delete Item'),
    #path('EditItem/<int:product_id>/', views.handle_edit_item_request, name='Edit Item')
]
