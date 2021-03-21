from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounts import views as accounts_views
from dashboards import views as dashboard_views

from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path('', dashboard_views.home, name='home'),
    path('backtesting/', dashboard_views.backtesting, name='backtesting'),
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', accounts_views.register, name='register'),

    url(r'^ajax/getUpdatedOHLC/$', dashboard_views.getUpdatedOHLC, name='getUpdatedOHLC'),
]