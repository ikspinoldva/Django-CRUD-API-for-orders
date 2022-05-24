from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('',
         RedirectView.as_view(pattern_name='orders:order-list'),
         name='dashboard'),
    path('orders/',
         include(('orders.urls', 'orders'), namespace='orders')),
]
