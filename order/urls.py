from django.urls import path

from order.views import BuyItemView, AddItemToCart, SubItemFromCart

urlpatterns = [
    path(r'buy/<int:pk>/', BuyItemView.as_view(), name='item_buy'),
    path(r'cart/add/<int:pk>/', AddItemToCart.as_view(), name='add_item_to_cart'),
    path(r'cart/sub/<int:pk>/', SubItemFromCart.as_view(), name='sub_item_form_cart'),
]

