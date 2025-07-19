from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListView.as_view()),
    path('products/<int:pk>', views.ProductDetailView.as_view()),
    path('products/info/', views.product_info),
    path('orders/',views.OrderListView.as_view()),
    path('user-orders/',views.UserOrderListView.as_view()),

]