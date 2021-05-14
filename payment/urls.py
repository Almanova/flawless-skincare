from django.urls import path
from payment import views


urlpatterns = [
    path('client_token/', views.braintree_client_token),
    path('checkout/', views.braintree_checkout),
]
