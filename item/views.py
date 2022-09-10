import os

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
        """Overwritten for sending Stripe Public API Key to front"""
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['API_KEY_PK'] = os.environ.get('API_KEY_PK', f'api_key')
        return context
