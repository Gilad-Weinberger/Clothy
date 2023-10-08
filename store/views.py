from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, FollowImage, Category, Cart, CartItem
from django.db.models import Avg, Q, Count
from django.http import HttpResponseBadRequest
from accounts.models import CustomUser
from django.contrib.auth.decorators import login_required

def Home(request):
    random_product = Product.objects.order_by('?').first()

    top_rated_products = Product.objects.annotate(
        avg_rating=Avg('comments__rating')
    ).order_by('-avg_rating')[:4]

    top_created_products = Product.objects.order_by('-created_at')[:4]
    follow_images = FollowImage.objects.all()[:5]

    if request.user.is_authenticated:
        try:
            user_profile = CustomUser.objects.get(email=request.user.email)
        except CustomUser.DoesNotExist:
            user_profile = None
    else:
        user_profile = None

    context = {
        'random_product': random_product,
        'top_rated_products': top_rated_products,
        'top_created_products': top_created_products,
        'follow_images': follow_images,
        'user_profile': user_profile,  
    }

    return render(request, 'store/home.html', context)


def Products(request):
    all_products = Product.objects.all()
    all_categories = Category.objects.all()

    category_id = request.GET.get('category')
    min_price = request.GET.get('min-price')
    max_price = request.GET.get('max-price')
    sort_by = request.GET.get('sort_by')
    search_query = request.GET.get('search') 

    filters = {}

    if category_id:
        filters['categories__id'] = category_id

    if min_price:
        filters['price__gte'] = min_price

    if max_price:
        filters['price__lte'] = max_price

    
    search_filters = Q()
    if search_query:
        search_filters |= Q(name__icontains=search_query) | Q(description__icontains=search_query)
    
    filtered_products = all_products.filter(**filters).filter(search_filters)

    filtered_products = filtered_products.annotate(
        avg_rating=Avg('comments__rating')
    ).annotate(
        num_ratings=Count('comments')
    )

    if sort_by == 'price_low_to_high':
        filtered_products = filtered_products.order_by('price')
    elif sort_by == 'price_high_to_low':
        filtered_products = filtered_products.order_by('-price')
    elif sort_by == 'newest':
        filtered_products = filtered_products.order_by('-created_at')
    elif sort_by == 'popularity':
        filtered_products = filtered_products.order_by('-avg_rating', '-num_ratings')

    if filters or search_filters:
        context = {
            'all_products': filtered_products,
            'all_categories': all_categories,
            'search_query': search_query
        }
    else:
        context = {
            'all_products': all_products,
            'all_categories': all_categories
        }

    return render(request, 'store/products.html', context)

def Product_Details(request, product_id): 
    product = get_object_or_404(Product, id=product_id)
    has_discount = (product.discount_type != 'none')

    context = {
        'product': product,
        'has_discount': has_discount,
    }

    return render(request, 'store/product_details.html', context)


@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.product.final_price * item.quantity for item in cart_items)
    cart_count = cart_items.count()

    context = {
        'cart_items': cart_items,
        'cart': cart,
        'total_price': total_price,
        'cart_count': cart_count,
    }

    return render(request, 'store/cart.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = request.POST.get('quantity', 1)

    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError()
    except ValueError:
        return HttpResponseBadRequest("Invalid quantity")

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(product=product)

    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    cart.items.add(cart_item)
    cart.save()

    return redirect('cart')


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()

    return redirect('cart')