from django.contrib import admin
from .models import *


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(SupplierModel)
class SupplierModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')
    search_fields = ('name', 'email', 'phone_number')
    ordering = ('name',)


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'supplier', 'price', 'quantity', 'article', 'available')
    list_filter = ('category', 'supplier', 'available')
    search_fields = ('name', 'article')
    ordering = ('category', 'quantity')
    list_editable = ('price', 'quantity', 'available')
    
    
@admin.register(AddressModel)
class AddressModelAdmin(admin.ModelAdmin):
    list_display = ('country', 'city', 'street', 'house')
    search_fields = ('country', 'city', 'street', 'house')
    ordering = ('country', 'city', 'street',)


@admin.register(CustomerModel)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'date_joined', 'deleted')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    list_filter = ('deleted',)
    list_editable = ('deleted',)


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_date', 'customer')
    search_fields = ('customer__first_name', 'customer__last_name', 'customer__email')
    ordering = ('-order_date',)
