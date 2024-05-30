from django.urls import path
from .views import(
    CheckoutView,
    CreateCheckoutSessionView,
    InvoiceView,
    OrderHistoryView,
    )

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('invoice/', InvoiceView.as_view(), name='invoice'),
    path('create-checkout-session', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('payment-success/', CreateCheckoutSessionView.paymentSuccess, name='payment-success'),
    path('payment-cancel/', CreateCheckoutSessionView.paymentCancel, name='payment-cancel'),
    path('webhook/stripe/', CreateCheckoutSessionView.my_webhook_view, name='webhook'),
    path('order-history/', OrderHistoryView, name='order_history'),
]