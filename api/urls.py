from django.urls import path
from example import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('admin/', views.admin_view, name='admin'),
    path('logbook/', views.logbook_view, name='logbook'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_info/',views.admin_info,name='admin_info'),
    path('user_data',views.user_data,name='user_data'),
]
