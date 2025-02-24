from django.contrib import admin
from .models import Item, Cart, CartItem

# Customize the Item model admin interface
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'location')
    list_filter = ('category', 'stock', 'location')
    search_fields = ('name', 'description')
    prepopulated_fields = {'description': ('name',)}  # Optional: for auto-filled descriptions based on name

admin.site.register(Item, ItemAdmin)

# Customize the CartItem model admin interface
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'item', 'quantity', 'size_in_kg')
    list_filter = ('cart', 'item')
    search_fields = ('cart__user__username', 'item__name')

admin.site.register(CartItem, CartItemAdmin)

# Register the Cart model (simple admin view)
admin.site.register(Cart)
