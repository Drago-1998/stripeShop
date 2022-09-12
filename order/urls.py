from django.urls import path

from order.views import BuyItemView, AddItemToCart, SubItemFromCart, CreateOrderFromCart, OrderDetail, PayFromOrder, \
    OrderListView

urlpatterns = [
    path(r'buy/<int:pk>/', BuyItemView.as_view(), name='item_buy'),
    path(r'cart/add/<int:pk>/', AddItemToCart.as_view(), name='add_item_to_cart'),
    path(r'cart/sub/<int:pk>/', SubItemFromCart.as_view(), name='sub_item_form_cart'),
    path(r'order/create/<str:currency>/', CreateOrderFromCart.as_view(), name='create_order_from_cart'),
    path(r'order/detail/<int:pk>/', OrderDetail.as_view(), name='order_detail'),
    path(r'order/pay/<int:pk>/', PayFromOrder.as_view(), name='order_pay'),
    path(r'order/list/', OrderListView.as_view(), name='order_list'),
]
