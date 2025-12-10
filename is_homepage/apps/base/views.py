from django.http import HttpResponse

def ratelimited_error_view(request, exception):
    return HttpResponse('Access Denied, Too Many Requests.', status=429)
