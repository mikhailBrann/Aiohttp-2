# Домашнее задание к лекции «Aiohttp»

1) запускаем docker для ДБ сервера:
```bash
    docker-compose up -d --build
```
2) устанавливаем нужные библиотеки:
```bash
    pip install -r requirements.txt
``` 
3) запускаем само приложение через gunicorn:
```bash
    python app.py
``` 

## Запросы:
 примеры запросов для работы с api в файле requests-examples.http