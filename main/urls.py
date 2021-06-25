from django.urls import path, include
from .views import HomeView, ShowRating, WebsiteDetailView, AddWebsiteView, UpdateWebsiteView, DeleteWebsiteView, AddCommentView, \
    call_model


urlpatterns = [
    #path('', views.home, name="home"),
    path('', HomeView.as_view(), name="home"),
    path('<slug>/<int:pk>', WebsiteDetailView.as_view(), name="Selected-Website"),
    path('create/', AddWebsiteView.as_view(), name="Add-Website"),
    path('edit/<slug>/<int:pk>', UpdateWebsiteView.as_view(), name="Update-Website"),
    path('<slug>/<int:pk>/delete', DeleteWebsiteView.as_view(), name="Delete-Website"),
    path('<slug>/<int:pk>/comment/', AddCommentView.as_view(), name="add_comment"),
    path('ratings/<slug>/<int:pk>', ShowRating.as_view(), name="show_rating"),
    path('model/', call_model.as_view()),
]
