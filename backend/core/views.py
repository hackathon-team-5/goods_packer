from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def page_not_found(request: HttpRequest, exception) -> HttpResponse:
    """
    This function is used to handle 404 errors, which occur when a requested
    page is not found. It takes in the request object and an exception as
    parameters and returns a rendered 404 error page with the path of the
    requested page. The function also sets the HTTP response status code
    to 404.
    """
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def csrf_failure(request: HttpRequest, reason='') -> HttpResponse:
    """
    This function is used to handle CSRF (Cross-Site Request Forgery) failures
    in Django. It takes in a request object and a reason (optional) and
    returns a rendered HTML template for a 403 error page. The 403 error
    page is displayed when a user tries to make a request that fails the
    CSRF check. The function is intended to provide a clear and user-friendly
    message to the user about why their request failed.
    """
    return render(request, 'core/403csrf.html')
