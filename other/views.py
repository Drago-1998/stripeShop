from django.http import JsonResponse
from django.views import View

from other.logic import add_promo_code, delete_promo_code


class AddPromoCode(View):
    """Add PromoCode to session"""
    def get(self, request, code):
        promo_response = add_promo_code(request.session.get('promos', False), code)

        if isinstance(promo_response, JsonResponse):
            return promo_response

        request.session['promos'] = promo_response
        return JsonResponse({
            'status': 'Ok',
            'promo': request.session['promos'],
        })


class DeletePromoCode(View):
    """Remove PromoCode from session"""
    def get(self, request, code):
        request.session['promos'] = delete_promo_code(request.session['promos'], code)
        return JsonResponse({
            'status': 'Ok',
            'promo': request.session['promos'],
        })
