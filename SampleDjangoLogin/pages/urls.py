from django.urls import path
#from pages import views
from . import views
from .views import stock_details

urlpatterns = [
    path('', views.index, name='index'),
    path("home/", views.home, name='home'),
    path("portfolio/", views.portfolio, name='portfolio'),
    path('watchlist/', views.user_watchlist2, name='user_watchlist'),
    path("notifications/", views.notifications, name='notifications'),
    path('stock/', views.stock_details, name='stock_details'),
    path('trade/execute/', views.execute_trade, name='execute_trade'),
    path('watchlist/toggle/<int:stock_id>/', views.toggle_watchlist, name='toggle_watchlist'),
    
    #path('EditItem/<int:product_id>/', views.handle_edit_item_request, name='Edit Item')
]
