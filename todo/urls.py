from django.contrib import admin
from django.urls import path
from todoList.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",SingupView.as_view(),name="singup"),
    path("home/",homeView,name="home"),
    path("logout/",logoutView,name="logout"),
    path("login/",loginView,name="login"),
    path("/delete/<int:id>/",delete,name="delete"),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)