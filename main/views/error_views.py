"""
Error views.

Functions and pages related to errors.
"""

from .functions import *


def page_404(request, exception: Exception) -> HttpResponse:
    """
    Page 404 view.
    """

    return render(request, 'pages/error/page_404.html')


def page_403(request, exception: Exception) -> HttpResponse:
    """
    Page 403 view.
    """

    return render(request, 'pages/error/page_403.html')


def page_500(request) -> HttpResponse:
    """
    Page 500 view.
    """

    return render(request, 'pages/error/page_500.html')


def error_page(request) -> HttpResponse:
    """
    Error page view.
    """

    return render(request, 'pages/error/error.html')
