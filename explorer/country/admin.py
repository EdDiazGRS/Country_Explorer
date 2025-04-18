from django.contrib import admin
from .models import Country

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'capital_city', 'population', 'language', 'currency')
    list_filter = ('currency', 'language')
    search_fields = ('name', 'capital_city', 'language')
    ordering = ('name',)


