from .models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        try:
            # Assuming the user model has a one-to-one relationship to a cart
            cart = request.user.cart
            return {'cart_item_count': cart.items.count()}
        except Cart.DoesNotExist:
            # If the user has no cart yet
            return {'cart_item_count': 0}
    # For anonymous users
    return {'cart_item_count': 0}