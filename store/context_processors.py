from accounts.models import CustomUser  
from .models import Cart  

def cart_count(request):
    if request.user.is_authenticated:
        try:
            user_cart = Cart.objects.get(user=request.user)
            cart_count = user_cart.items.count()  
        except Cart.DoesNotExist:
            cart_count = 0
    else:
        cart_count = 0

    return {'cart_count': cart_count}
