from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListViewListCreateAPIView.as_view()),
    path('products/<int:pk>', views.ProductDetailView.as_view()),
    path('products/info/', views.ProductInfoAPIView.as_view()),
    path('orders/',views.OrderListView.as_view()),
    path('user-orders/',views.UserOrderListView.as_view(), name='user-orders'),
]