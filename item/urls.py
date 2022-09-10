from django.urls import path

from item.views import ItemListView, ItemDetailView, BuyItemView

urlpatterns = [
    path(r'', ItemListView.as_view(), name='home'),
    path(r'item/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path(r'buy/<int:pk>/', BuyItemView.as_view(), name='item_buy'),
]
