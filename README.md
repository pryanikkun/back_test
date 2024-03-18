## Структура приложения
```shell
│   main.py       # конфигурация приложения
│   dependency.py # FastAPI авторизация
│   models.py     # модели
│   redis.py      # подключение и класс для работы с redis
│   __init__.py
│
├─── handler         # Настройка бота, ответы на комманды
│      bot.py
│      utils.py
│      __init__.py
│
├─── config         # Настройки
│       __init__.py
│
├─── management   
│       create_employee.py    # Создание сотрудника
│
├─── service      # Лежат функции, использующиеся при запуске/завершении сессии 
│       utils.py
│       __init__.py
│
└─── views   #Лежат вьюшки и схемы 
    ├── schemas    # Схемы pydantic
    │       __init__.py   
    ├── crud 
    │       clients.py
    │       employees.py
    │       messages.py
    │       tickets.py
    │   main.py
    │   __init__.py
```
## Подготовка приложения
#### 1. Получение TG_ACCESS_URL
Я использовала ngrok для создания туннеля

Команда
```
ngrok http http://127.0.0.1:8000
```
Копируем URL https://... и вставляем в TG_ACCESS_URL
#### 1. В папке /web создать файл ```.env``` с переменными
````
TG_BOT_TOKEN

POSTGRES_HOST
POSTGRES_PORT
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB

TG_ACCESS_URL
````
### 2. Запуск для разработки
#### 2.1. Меняем хост
В [__init__.py](src%2Fapp%2Fconfig%2F__init__.py) 
указываем ```HOST = '127.0.0.1'``` вместо ```HOST = '0.0.0.0'```

#### 2.2. Запуск Docker
Запускаем команду в терминале
```
docker-compose up
```
Отключаем контейнер web (он не работает)
#### 2.3. Запускаем __main__.py
Запускаем команду в терминале
```
python __main__.py
```

### 3.Миграции
#### Первый запуск
```shell
> aerich init -t app.conf.DATABASE
Success create migrate location ./migrations
Success write config to pyproject.toml

> aerich init-db
Success create app migrate location migrations/models
Success generate schema for app "models"
```
### requirements.txt
```requirements.txt
uvicorn==0.28.0
pydantic==2.5.3
aiogram==3.4.1
fastapi==0.110.0
pydantic-settings==2.2.1
tortoise-orm==0.20.0
asyncpg==0.27.0
aerich==0.7.1
asyncio-redis==0.16.0
requests==2.31.0
```



