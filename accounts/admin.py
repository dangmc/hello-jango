from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email',)
    ordering = ['name']
    search_fields = ['name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer', 'product']
    list_display = ('customer', 'product', 'status',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    ordering = ['name']
    search_fields = ['name']
    list_display = ('name', 'price', 'category')


admin.site.register(Tag)
