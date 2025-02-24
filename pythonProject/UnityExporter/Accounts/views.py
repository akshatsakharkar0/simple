

# Create your views here.
# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm



def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("Form is valid")
            login(request, user)  # Automatically log the user in after registration
            return redirect('home')


    else:


        form = UserRegistrationForm()
        print(form.errors)
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to homepage or dashboard
            else:
                messages.error(request, 'Invalid credentials')
        else:
            messages.error(request, 'Invalid credentials')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')  # Redirect to homepage after logout


# View to display all items

from .models import Item, Cart, CartItem
from .forms import AddToCartForm
from django.contrib.auth.decorators import login_required


# View to display items by category
def items_view(request):
    categories = ['turmeric', 'chilli', 'coriander', 'biomass']
    category_filter = request.GET.get('category')  # Get the category from the query parameters

    if category_filter and category_filter in categories:
        # If a specific category is requested, filter items by that category
        items_by_category = {category_filter: Item.objects.filter(category=category_filter)}
    else:
        # Otherwise, show all categories with their respective items
        items_by_category = {category: Item.objects.filter(category=category) for category in categories}
    context = {
        'items_by_category': items_by_category,
        'categories': categories,
        'current_category': category_filter
    }

    return render(request, 'shop/items.html', context)

# View to add item to cart
from django.http import JsonResponse

@login_required
def add_to_cart(request, item_id):
    # Get the item the user wants to add
    item = get_object_or_404(Item, id=item_id)
    # Get the user's cart or create a new one
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Check if the item is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        # If the item is already in the cart, increase the quantity
        cart_item.quantity = 1
        cart_item.save()
    # Redirect back to the items page
    return redirect('items_view')

# View to display cart
@login_required
def cart_view(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    total_price = sum(cart_item.item.price * cart_item.quantity for cart_item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,

    }
    return render(request, 'shop/cart.html', context)


# View to remove item from cart
from django.http import JsonResponse


@login_required
def remove_from_cart(request, cart_item_id):
    # Get the user's cart
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        cart_item.delete()

        # Redirect back to the cart view
        return redirect('cart_view')


# View to update cart item (quantity/size)
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
def update_cart(request, cart_item_id):
    # Get the item the user wants to add

    # Check if the item is already in the cart
    cart_item= CartItem.objects.get(id=cart_item_id, cart__user=request.user)


    # Redirect back to the items page
    quantity = request.POST.get('quantity')
    size_in_kg = request.POST.get('size_in_kg')
    # Validate that the quantity is an integer and greater than 0
    quantity = int(quantity)
    cart_item.quantity = quantity

    size_in_kg = int(size_in_kg)
    cart_item.size_in_kg = size_in_kg

    cart_item.save()
    return redirect('cart_view')
