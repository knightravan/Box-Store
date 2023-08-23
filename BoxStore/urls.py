from django.contrib import admin
from django.urls import path,include

from Inventory import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('boxes/', views.BoxList.as_view(), name='box-list'),
    path('auth/',include('rest_framework.urls')),
    path('boxes/<int:pk>/', views.BoxDetail.as_view(), name='box-detail'),
    path('boxes/myboxes/', views.MyBoxList.as_view(), name='my-box-list'),
    path('', views.index, name='boxlist'),


    path('dashboard/', views.dashboard, name="dashboard"),
    path('login/', views.user_login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.user_logout, name="logout"),
    path('addbox/', views.addpost, name="addpost"),
    path('updatepost/<int:id>/', views.updatepost, name="updatepost"),
    path('deletepost/<int:id>/', views.deletepost, name="deletepost"),

    ]
