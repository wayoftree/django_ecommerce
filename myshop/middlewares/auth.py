from django.shortcuts import redirect


def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        print(request.session.get('customer'))
        returnUrl = request.META['PATH_INFO']
        print(request.META['PATH_INFO'])
        if not request.session.get('customer'):
           return redirect(f'/customer_login?next={returnUrl}')

        response = get_response(request)
        return response

    return middleware
