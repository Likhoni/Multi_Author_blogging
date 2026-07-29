from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages


def author_required(view_func):
    """
    Decorator for views that checks that the logged-in user is an Author or Superuser.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access the author area.")
            return redirect('login')
        if not (request.user.is_author or request.user.is_superuser):
            messages.error(request, "Access denied. Only approved authors can perform this action.")
            raise PermissionDenied("Only approved authors can perform this action.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def admin_required(view_func):
    """
    Decorator for views that checks that the logged-in user is a Superuser / Admin.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access the Admin Panel.")
            return redirect('login')
        if not request.user.is_superuser:
            messages.error(request, "Access denied. Only site administrators can access the Admin Panel.")
            raise PermissionDenied("Only site administrators can access the Admin Panel.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
