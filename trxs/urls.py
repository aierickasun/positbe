from django.urls import path, include
from trxs import views
from trxs import transaction_engine

urlpatterns = [
    path('transactions/',views.TrxsList.as_view()),
    path('transactions/<int:pk>',views.TrxsDetail.as_view()),
    path('transactions-receipt/<int:pk>',views.TrxsReceiptDetail.as_view()),
    path('transaction-engine/',transaction_engine.TransactionEngine.as_view())
]
