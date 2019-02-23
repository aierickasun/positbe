from django.urls import path, include
from prices import views

urlpatterns = [
    path('prices/',views.PricesList.as_view()),
    path('prices/<int:pk>/',views.PricesDetail.as_view())
]
