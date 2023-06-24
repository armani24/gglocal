from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    # Add other URL patterns if needed
    path('logout/', views.logout_view, name='logout'),
    path('register/as/owner/', views.register_owner, name='register_owner'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('my/dashboard/', views.owner_dash, name='owner_dash'),
    path('owner/profile/', views.owner_profile, name='owner_profile'),
    path('owner/messages/', views.owner_msgs, name='owner_msgs'),
    path('owner/messages/<int:id>', views.owner_msgs, name='owner_msgs_details'),
    #guide
    path('guide/profile/', views.guide_profile, name='guide_profile'),
    path('main/dashboard/', views.guide_dash, name='guide_dash'),
    path('main/dashboard/guide/msgs/', views.guide_msgs, name='guide_msgs'),
    path('main/dashboard/msgs/details/<int:id>', views.guide_msgs, name='guide_msg_details'),
    #customer
    path('customer/profile/', views.customer_profile, name='customer_profile'),
    path('customer/dashboard/', views.customer_dash, name='customer_dash'),
    path('customer/dashboard/ms/<int:id>', views.customer_dash, name='msg_details'),
    # other URL patterns
]