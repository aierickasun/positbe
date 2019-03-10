from django.urls import path, include
from inventories import views

urlpatterns = [
    path('inventories/',views.InventoriesList.as_view()),
    path('inventories/<int:pk>',views.InventoriesDetail.as_view())
]
