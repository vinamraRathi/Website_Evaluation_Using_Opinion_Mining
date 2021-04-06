from django.urls import path
from .views import HomeView, WebsiteDetailView, AddWebsiteView, UpdateWebsiteView, DeleteWebsiteView

urlpatterns = [
    #path('', views.home, name="home"),
    path('', HomeView.as_view(), name="home"),
    path('<slug>/<int:pk>', WebsiteDetailView.as_view(), name="Selected-Website"),
    path('create/', AddWebsiteView.as_view(), name="Add-Website"),
    path('edit/<slug>/<int:pk>', UpdateWebsiteView.as_view(), name="Update-Website"),
    path('<slug>/<int:pk>/delete', DeleteWebsiteView.as_view(), name="Delete-Website"),
]
