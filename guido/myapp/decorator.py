from django.contrib import messages
from django.utils.translation import gettext as _


def is_owner_decorator(func):
    def wrapper(user, *args, **kwargs):
        # Assuming 'user' is an object that represents the user
        if user.is_owner:
            return func(user, *args, **kwargs)
        else:
            raise Exception("Access denied. You are not the owner.")

    return wrapper




from django.shortcuts import redirect

def owner_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Assuming you have a 'User' model with an 'is_owner' field
        if request.user.is_authenticated and request.user.is_owner:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('myapp:home')  # Replace 'home' with the name of your home page URL or view

    return wrapper


def guide_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Assuming you have a 'User' model with an 'is_owner' field
        if request.user.is_authenticated and request.user.is_guid:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('myapp:home')  # Replace 'home' with the name of your home page URL or view

    return wrapper

def customer_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Assuming you have a 'User' model with an 'is_owner' field
        if request.user.is_authenticated and request.user.is_customer:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('myapp:home')  # Replace 'home' with the name of your home page URL or view

    return wrapper