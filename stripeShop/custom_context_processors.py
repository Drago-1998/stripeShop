from order.logic import cart_items_info


def cart_context(request):
    """Add cart to all contexts"""
    return {
        'cart': cart_items_info(request.session.get('cart', {})),
    }


def promo_context(request):
    """Add promos to all contexts"""
    return {
        'promos': request.session.get('promos', {}).values(),
    }
