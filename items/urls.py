from django.urls import path, include
from items import views

urlpatterns = [
    path('items/',views.ItemsList.as_view()),
    path('items/<int:pk>/',views.ItemsDetail.as_view())
]
