#!/usr/bin/env python3
"""
API Tester - простая замена Postman для тестирования API
"""
import requests
import json
from datetime import datetime

def test_api(url, method="GET", headers=None, data=None, description="API Test"):
    """Тестирует API и выводит результат"""
    print(f"\n{'='*50}")
    print(f"🔍 {description}")
    print(f"📡 {method} {url}")
    print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*50}")
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=10)
        
        # Статус
        status_emoji = "✅" if response.status_code < 400 else "❌"
        print(f"{status_emoji} Статус: {response.status_code}")
        
        # Заголовки
        print(f"📋 Content-Type: {response.headers.get('content-type', 'неизвестно')}")
        print(f"📏 Размер: {len(response.content)} байт")
        
        # Тело ответа
        content_type = response.headers.get('content-type', '')
        if 'application/json' in content_type:
            print(f"📄 JSON Response:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        elif 'text' in content_type:
            print(f"📄 Text Response:")
            print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
        else:
            print(f"📄 Binary Response: {len(response.content)} байт")
            
    except requests.exceptions.Timeout:
        print("⏱️ ТАЙМАУТ: Сервер не отвечает")
    except requests.exceptions.ConnectionError:
        print("🚫 ОШИБКА СОЕДИНЕНИЯ: Не удается подключиться")
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")

def main():
    """Основная функция для тестирования API"""
    print("🚀 API Tester - Простая замена Postman")
    print("Тестируем популярные API...")
    
    # Тест Dog API
    test_api(
        "https://dog.ceo/api/breeds/image/random",
        description="🐕 Dog API - Случайная собачка"
    )
    
    # Тест Cat API
    test_api(
        "https://cataas.com/cat",
        description="🐱 Cat API - Случайный котик"
    )
    
    # Тест JSONPlaceholder
    test_api(
        "https://jsonplaceholder.typicode.com/posts/1",
        description="📝 JSONPlaceholder - Тестовый пост"
    )
    
    print(f"\n{'='*50}")
    print("✨ Тестирование завершено!")
    print("💡 Для своих API замените URL в функции test_api()")

if __name__ == "__main__":
    main()