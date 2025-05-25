# Конструирование программного обеспечения. Контрольная работа №2

## Работу выполнил **Девятов Денис Сергеевич, группа БПИ-238**

---

## Инструкция запуска.

Находясь в корне проекта, выполните в терминале:

```
docker compose up --build
```

После старта контейнеров можно открыть Postman и проверить работу сервисов.

---

## 1. Соответствие ключевым критериям

* **Функциональность (2 б.)**

  * **FileStoringService**: приём файлов `.txt`, дедупликация через SHA-256 (антиплагиат 100 %), отдача файла по стриму
  * **FileAnalysisService**: вычисление числа абзацев, слов и символов; по желанию — генерация облака слов

* **Микросервисная архитектура (4 б.)**

  * Два автономных микросервиса: FileStoringService и FileAnalysisService
  * Единая точка входа через Nginx API Gateway
  * Отдельные базы PostgreSQL на портах 5432 и 5433
  * Обработка ошибок: 404, 409, 422, 503, 500

* **Swagger / Postman (1 б.)**

  * Автодокументация Swagger UI на `/docs` для каждого сервиса
  * Коллекция Postman в папке `postman/`

* **Качество кода и документации (2 б.)**

  * Чистое разделение на слои (Domain, Use Cases, Infrastructure, Presentation)
  * Подробные README в каждом сервисе и этот общий отчёт в Markdown

* **Тестирование и покрытие ≥ 65 % (1 б.)**

  * Unit-тесты для бизнес-логики
  * Общий процент покрытия \~ 85 % в каждом сервисе

---

## 2. Роль API Gateway (Nginx)

API Gateway на базе Nginx распределяет запросы между микросервисами:

```nginx
http {
    upstream file_storing_service {
        server file_storing_service:8000;
    }
    upstream file_analisys_service {
        server file_analisys_service:8001;
    }

    server {
        listen 80;
        
        location /file_storing_service/ {
            proxy_pass http://file_storing_service/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        
        location /file_analisys_service/ {
            proxy_pass http://file_analisys_service/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}

events {}
```
