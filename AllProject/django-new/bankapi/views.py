from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def api_test(request):
    if request.method == "GET":
        return JsonResponse({
            "message": "Django API работает!",
            "status": "success",
            "data": {
                "service": "Bank API",
                "version": "1.0",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        })
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            return JsonResponse({
                "message": "Данные получены",
                "status": "success",
                "received_data": data
            })
        except:
            return JsonResponse({
                "message": "Ошибка в данных",
                "status": "error"
            }, status=400)
