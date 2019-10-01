from django.urls import path
from transactionsapp import views

app_name = 'transactionsapp'


urlpatterns = [
    path('phone_transaction', views.MakePhoneTransactionView.as_view(), name='phone_transaction'),
    path('callback',views.transaction_callback,name="transaction_callback")
]
