from django.urls import path, include
from stores import views

urlpatterns = [
    path('stores/',views.StoresList.as_view()),
    path('stores/<int:pk>/',views.StoresDetail.as_view())
]
