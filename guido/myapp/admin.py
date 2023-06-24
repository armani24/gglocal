from django.contrib import admin

# Register your models here.
from .models import ListingCategory, Listing, City

admin.site.register(ListingCategory)
admin.site.register(Listing)
admin.site.register(City)
