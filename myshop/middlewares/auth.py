from django.shortcuts import redirect


def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if not request.session.get('customer'):
            return redirect('customer_login')
        response = get_response(request)
        return response

        # Code to be executed for each request/response after
        # the view is called.

    return middleware

    return middleware
