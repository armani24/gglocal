from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('add/listing/', views.create_listing, name='create_listing'),
    path('listing/review/', views.listing_list, name='listing_list'),
    path('listing/review/<str:categ>/<str:city>', views.listing_list, name='listing_list_filter'),
    path('listing/review/<int:id>/', views.listing_details, name='listing_details'),
    path('my/listings/review/', views.my_listings, name='my_listings'),
    path('delete/listings/<int:id>/', views.delete_listing, name='delete_listing'),
    path('edit/listings/<int:id>/', views.edit_listing, name='edit_listing'),
    path('guides/list/', views.guides_list, name='guides_list'),
    path('guides/list/<str:city>', views.guides_list, name='guides_list_city'),
    path('guide/details/<int:id>/', views.guide_details, name='guide_details'),
    path('review/d/details/<int:id>/', views.del_revguide, name='del_revguide'),
    # Add other URL patterns if needed
    path('about/us/', views.about_us, name='about_us'),
]
