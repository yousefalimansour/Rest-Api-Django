from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('products/', views.ProductListViewListCreateAPIView.as_view()),
    path('products/<int:product_id>', views.ProductDetailView.as_view()),
    path('products/info/', views.ProductInfoAPIView.as_view()),
     path('users/',views.UserAPIView.as_view()),

    # path('orders/',views.OrderListView.as_view()),
    # path('user-orders/',views.UserOrderListView.as_view(), name='user-orders'),
]

router = DefaultRouter()
router.register('orders',views.OrderViewSet)
urlpatterns += router.urls
