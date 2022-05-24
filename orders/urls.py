from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import path, reverse_lazy
from .models import Order, Category
from .views import OrderListView, CategoryListView


urlpatterns = [
    path('order/list/',
         OrderListView.as_view(),
         name='order-list'),
    path('order/create/',
         CreateView.as_view(
            model=Order,
            fields='__all__',
            success_url=reverse_lazy('orders:expense-list'),
            template_name='generic_update.html'
         ),
         name='order-create'),
    path('order/<int:pk>/edit/',
         UpdateView.as_view(
            model=Order,
            fields='__all__',
            success_url=reverse_lazy('orders:order-list'),
            template_name='generic_update.html'
         ),
         name='order-edit'),
    path('order/<int:pk>/delete/',
         DeleteView.as_view(
            model=Order,
            success_url=reverse_lazy('orders:order-list'),
            template_name='generic_delete.html'
         ),
         name='order-delete'),

    path('category/list/',
         CategoryListView.as_view(),
         name='category-list'),
    path('category/create/',
         CreateView.as_view(
            model=Category,
            fields='__all__',
            success_url=reverse_lazy('orders:category-list'),
            template_name='generic_update.html'
         ),
         name='category-create'),
    path('category/<int:pk>/edit/',
         UpdateView.as_view(
             model=Category,
             fields='__all__',
             success_url=reverse_lazy('orders:category-list'),
             template_name='generic_update.html'
         ),
         name='category-edit'),
    path('category/<int:pk>/delete/',
         DeleteView.as_view(
            model=Category,
            success_url=reverse_lazy('orders:category-list'),
            template_name='generic_delete.html'
         ),
         name='category-delete'),
]
