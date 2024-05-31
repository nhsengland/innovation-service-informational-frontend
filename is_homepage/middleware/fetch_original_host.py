class FetchOriginalHostMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    if 'HTTP_X_ORIGINAL_HOST' in request.META:
      request.META['HTTP_HOST']=request.META['HTTP_X_ORIGINAL_HOST']
      
    return self.get_response(request)
