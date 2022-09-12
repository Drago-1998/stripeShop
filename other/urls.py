from django.urls import path

from other.views import AddPromoCode, DeletePromoCode

urlpatterns = [
    path(r'promo/activate/<str:code>/', AddPromoCode.as_view(), name='activate_promo'),
    path(r'promo/deactivate/<str:code>/', DeletePromoCode.as_view(), name='deactivate_promo'),
]
