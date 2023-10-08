from django.contrib import admin
from .models import Product, Color, Category, FollowImage
from .forms import ProductForm # Import the custom widget

def duplicate_selected_items(modeladmin, request, queryset):
    for item in queryset:
        new_product = Product(
            name=item.name,
            description=item.description,
            price=item.price,
            discount_type=item.discount_type,
            discount_value=item.discount_value,
            multiple_colors=item.multiple_colors,
            image=item.image,
        )
        
        new_product.save()  # Save the new product to generate a new product_id
        new_product.categories.set(item.categories.all())
        new_product.colors.set(item.colors.all())
        
    modeladmin.message_user(request, f"{len(queryset)} items duplicated successfully.")

duplicate_selected_items.short_description = "Duplicate selected items"


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'price', 'created_at')
    actions = [duplicate_selected_items]
    form = ProductForm

class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_hex_code')

    def display_hex_code(self, obj):
        if "#" == obj.hex_code[0]:
            return f"{obj.hex_code}"
        else:
            return f"#{obj.hex_code}"
    display_hex_code.short_description = 'Hex Code'

admin.site.register(Product, ProductAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Category)
admin.site.register(FollowImage)