from django.contrib import admin
from .models import Category, Product, Reviews, Profile


admin.site.register(Profile)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated', 'producer', 'limited', 'category']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['name', 'timestamp', 'description']
    list_filter = ['name', 'timestamp', 'description']


admin.site.register(Reviews, ReviewsAdmin)
