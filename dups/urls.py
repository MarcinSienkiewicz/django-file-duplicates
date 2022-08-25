from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainView, name="main"),
    path('status/', views.statusView, name="status"),
    path('listing/', views.listingView, name='listing'),
    path('delete/', views.deleteView, name="delete"),
    path('show_errors/', views.showErrorsView, name="show-errors"),
]
