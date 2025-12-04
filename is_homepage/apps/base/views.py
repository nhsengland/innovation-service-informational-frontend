from django.http import HttpResponse

def ratelimited_error_view(request, exception):
    return HttpResponse('Rate limit exceeded. Please try again later.', status=429)
