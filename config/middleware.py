from django.shortcuts import render

class LandingFallbackMiddleware:
    """If a view returns 404 for a GET request, render the landing page.
    Temporary safety net while diagnosing Render routing.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            status = getattr(response, 'status_code', None)
        except Exception:
            status = None
        if request.method == 'GET' and status == 404:
            return render(request, 'landing.html', {})
        return response
