from django.http import JsonResponse
from django.views.decorators.http import require_safe


@require_safe
def healthz(request):
    response = JsonResponse({"status": "ok"})
    response["Cache-Control"] = "no-cache, no-store, max-age=0, private"
    return response
