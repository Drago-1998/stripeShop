import os

from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView, ListView

from item.models import Item


class ItemListView(ListView):
    model = Item
    context_object_name = 'items'
    template_name = 'item/list.html'
    paginate_by = 20


class ItemDetailView(DetailView):
    model = Item
    template_name = 'item/detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['API_KEY_PK'] = os.environ.get('API_KEY_PK', f'api_key')
        return context


class BuyItemView(View):

    def get(self, request, pk):
        import stripe

        stripe.api_key = os.environ.get('API_KEY_SK', f'api_key')

        item = Item.objects.get(id=pk)
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": item.price_id,
                    "quantity": 1,
                },
            ],
            success_url='http://localhost:8000/',
            cancel_url=f'http://localhost:8000/item/{pk}/',
            mode='payment'
        )
        return JsonResponse({
            'session': {
                'id': session.id,
                'url': session.url
            }
        })
