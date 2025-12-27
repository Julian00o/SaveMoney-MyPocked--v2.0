from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

@csrf_exempt
def api_root(request):
    return JsonResponse({
        'message': 'BankUp API',
        'endpoints': {
            'register': '/api/register/',
            'login': '/api/login/',
            'user': '/api/user/',
            'profile': '/api/profile/'
        }
    })

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received registration data:", data)
            
            # УПРОЩЕННАЯ ПРОВЕРКА
            required_fields = ['username', 'email', 'password']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({
                        'error': f'Field {field} is required'
                    }, status=400)
            
            # Автоматически устанавливаем password2 = password если его нет
            if 'password2' not in data:
                data['password2'] = data['password']
                print("Auto-setting password2 = password")
            
            # Проверка совпадения паролей
            if data.get('password') != data.get('password2'):
                return JsonResponse({
                    'error': 'Passwords do not match'
                }, status=400)
            
            # Проверка существования пользователя
            if User.objects.filter(username=data['username']).exists():
                return JsonResponse({
                    'error': 'User with this username already exists'
                }, status=400)
            
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({
                    'error': 'User with this email already exists'
                }, status=400)
            
            # Создание пользователя
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', '')
            )
            
            # УПРОЩЕННЫЙ ОТВЕТ - БЕЗ ТОКЕНА
            response_data = {
                'success': True,
                'message': 'User created successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }
            
            print("Registration successful:", response_data)
            return JsonResponse(response_data, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print("Registration error:", str(e))
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            from django.contrib.auth import authenticate
            
            data = json.loads(request.body)
            print("Login attempt:", data)
            
            user = authenticate(
                username=data.get('username'),
                password=data.get('password')
            )
            
            if user is not None:
                response_data = {
                    'success': True,
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    }
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({
                    'error': 'Invalid username or password'
                }, status=400)
                
        except Exception as e:
            print("Login error:", str(e))
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def user_info(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        })
    return JsonResponse({'error': 'Not authenticated'}, status=401)

@csrf_exempt
def profile(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name
            },
            'stats': {
                'accounts_count': 0,
                'total_balance': 0
            }
        })
    return JsonResponse({'error': 'Not authenticated'}, status=401)