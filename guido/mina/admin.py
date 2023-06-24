from django.contrib import admin
from .models import HomeSlider, HomeListing, ContactUs_info, AboutUS
# Register your models here.


admin.site.register(HomeSlider)

# class HomeListingInline(admin.TabularInline):
#     model = HomeListing.listing.through
#     extra = 1


# class HomeListingAdmin(admin.ModelAdmin):

#     #list_filter = ['category']
#     inlines = [HomeListingInline]


admin.site.register(HomeListing)
admin.site.register(ContactUs_info)
admin.site.register(AboutUS)