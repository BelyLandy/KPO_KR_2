# Конструирование программного обеспечения. Контрольная работа №2

## Работу выполнил **Девятов Денис Сергеевич, группа БПИ-238**

## Документация к разработанной системе антиплагиата.

---

## Инструкция запуска.

В корне проекта, выполните в терминале:

```
# Установка зависимостей для разработки.
python -m pip install -r requirements.txt -r requirements-dev.txt

# Сборка и запуск стека.
docker compose up --build -d

# Остановка и удаление томов.
docker compose down -v
```
![image](https://github.com/user-attachments/assets/6174c39e-4a01-4c3d-9757-fc4bec8aca76)
![image](https://github.com/user-attachments/assets/7386a0fa-a586-4bfa-8cc8-0508209f9f1a)
![image](https://github.com/user-attachments/assets/316d6627-e87b-49f9-b281-4b5ba2ac8453)


После запуска контейнеров можно открыть Swagger на 8001 и проверить работу решения.

| URL                                                      | Сервис                        |
| -------------------------------------------------------- | ----------------------------- |
| [http://localhost:8001/docs](http://localhost:8001/docs) | API Gateway (основной вход)   |
| [http://localhost:8000/docs](http://localhost:8000/docs) | File Storing Service          |
| [http://localhost:8002/docs](http://localhost:8002/docs) | File Analysis Service         |

![image](https://github.com/user-attachments/assets/f1e649af-d18b-4d90-bf03-a7a7bbf6fe79)

![image](https://github.com/user-attachments/assets/ba3a71cb-5a0e-476d-86c9-a2a2f9304aff)

![image](https://github.com/user-attachments/assets/417d568b-70a1-4de3-8461-adcd8989e3b9)


### Предварительные требования для развёртывания.

| ПО             | Версия                                |
| -------------- | ------------------------------------- |
| Docker Engine  | ≥ 24.0                                |
| Docker Compose | v2                                    |
| Python         | ≥ 3.10 (только для разработки/тестов) |

---

## Назначение системы.

Серверное приложение предназначено для автоматизированной обработки *.txt*-отчётов:

| № | Возможность             | Описание                                                                           |
| - | ----------------------- | ---------------------------------------------------------------------------------- |
| 1 | **Приём отчёта**        | `POST /files` — принимает `.txt`, сохраняет и возвращает `id` + признак дубликата. |
| 2 | **Статистика**          | `GET /analysis/{id}` — абзацы, слова, символы.`words` ≠ 0 проверено тестами.       |
| 3 | **100 % плагиат**       | SHA‑256 дубликация: повторная загрузка ⇒ тот же `id`, `is_duplicate=true`.         |
| 4 | **Word Cloud** *(доп.)* | PNG генерируется локально (библиотека *wordcloud*) и доступен `/wordcloud/{key}`.  |

---

## Архитектура системы.

![image](https://github.com/user-attachments/assets/345b576c-618c-4bf7-a0c1-7318db816a31)

```
docker-network
│
├─ gateway (0.0.0.0:8001)          – маршрутизация REST-запросов
│
├─ storing-service (8000)          – S3-хранение + Postgres-метаданные
│      └─ MinIO  (9000/9001)       – S3-совместимое хранилище
│
├─ analysis-service (8002)         – статистика, генерация word-cloud
│      └─ Redis (6379) + RQ-worker – очередь фоновых задач
│
└─ Postgres (5432)                 – единая БД метаданных
```

Каждый сервис — изолированный Docker-контейнер, конфигурируется через переменные окружения и взаимодействует только по HTTP внутри выделенной сети `docker-compose`.
*Ошибка любого сервиса* ловится Gateway’ем и конвертируется в `HTTP 5xx/4xx`.

---

## Справочник API (через Gateway :8001)

| Метод                        | Описание                                         |
| ---------------------------- | ------------------------------------------------ |
| **POST**  `/files`           | загрузить файл, получить `{id, is_duplicate, …}` |

![image](https://github.com/user-attachments/assets/368be796-fea0-44ab-94cf-7353eadc7423)
![image](https://github.com/user-attachments/assets/062574ee-661b-444b-8cda-a6a78f841b45)

| **GET**   `/files/{id}`      | скачать исходный файл                            |

![image](https://github.com/user-attachments/assets/825ce20e-52da-43c7-be9b-52110bd1dd79)
![image](https://github.com/user-attachments/assets/6c24bc7d-7a20-4c1c-aa48-7398591ab450)

| **POST**  `/analysis/{id}`   | инициировать анализ                              |

![image](https://github.com/user-attachments/assets/01033655-ce87-4dbf-babe-2111e6234f7d)


| **GET**   `/analysis/{id}`   | получить статус/результат                        |
| **GET**   `/wordcloud/{key}` | получить PNG-изображение                         |

Полные спецификации OpenAPI 3.1.0 расположены в каталоге **`docs/`**:

```
docs/
 ├─ openapi-gateway.json
 ├─ openapi-storing.json
 └─ openapi-analysis.json
```

Можно импортировать в Postman «Raw text» или откройте в Swagger‑Editor.

---

## Запуск автоматических тестов

```bash
# поднимет docker-stack, выполнит pytest, соберёт покрытие
pytest              # параметры задаются в pytest.ini
```

Покрытие по `coverage.py` ≥ **65 %**.

---

## Код-стайл и качество

* Инструменты проверки: **ruff format + ruff check**.
* Асинхронный доступ к I/O, отсутствуют блокирующие вызовы в event-loop.
* Разделение слоёв: маршрутизация, бизнес-логика, хранилище.

