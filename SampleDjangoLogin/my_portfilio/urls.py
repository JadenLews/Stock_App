"""
URL configuration for my_portfilio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views 
from django.urls import include, path
from pages import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("pages/", include("pages.urls")),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='pages/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='pages/logout.html',http_method_names = ['get', 'post', 'options']), name='logout'),
    path("home/", user_views.home, name='home'),
    path("portfolio/", user_views.portfolio, name='portfolio'),
    path('watchlist/', user_views.user_watchlist, name='user_watchlist'),
    path("notifications/", user_views.notifications, name='notifications'),
    path('stock/<str:symbol>/', user_views.stock_details, name='stock_details'),
    path('watchlist/toggle/<str:symbol>/', user_views.toggle_watchlist, name='toggle_watchlist'),
    path('trade/execute/', user_views.execute_trade, name='execute_trade'),
    path('trade/addwatchlist/', user_views.add_watchlist, name='add_watchlist'),
    path('notifications/', user_views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/', user_views.notifications, name='notification_detail'),
 ]
