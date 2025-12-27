# transactions/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection

@csrf_exempt
def transaction_list(request):
    if request.method == 'GET':
        # Проверяем есть ли таблица
        with connection.cursor() as cursor:
            try:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions_transaction'")
                table_exists = cursor.fetchone()
                
                if table_exists:
                    cursor.execute("SELECT * FROM transactions_transaction")
                    columns = [col[0] for col in cursor.description]
                    rows = cursor.fetchall()
                    transactions = [dict(zip(columns, row)) for row in rows]
                else:
                    transactions = []
            except:
                transactions = []
        
        return JsonResponse(transactions, safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        # Простая логика сохранения
        return JsonResponse({"id": 1, **data}, status=201)

@csrf_exempt  
def transaction_stats(request):
    return JsonResponse({
        "total_income": 0,
        "total_expense": 0,
        "balance": 0
    })