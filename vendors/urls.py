from django.urls import path, include
from vendors import views

urlpatterns = [
    path('vendors/',views.VendorsList.as_view()),
    path('vendors/<int:pk>/',views.VendorsDetail.as_view())
]
