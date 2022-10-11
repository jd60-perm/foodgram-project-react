# praktikum_new_diplom

### Описание проекта:

Приложение мини социальная сеть по обмену рецептами приготовления
блюд. Backend на фреймворке Django, Frontend на React.

### Шаблон наполнения env-файла:

Расположение файла: backend/foodgram/foodgram/.env
Данный файл используется для передачи в окружение
приложения следующих переменных без их явного указания в коде:

DB_ENGINE=<тип драйвера БД>
DB_NAME=<имя БД>
POSTGRES_USER=<имя пользователя БД>
POSTGRES_PASSWORD=<пароль пользователя БД>
DB_HOST=<имя хоста БД>
DB_PORT=<порт БД>


### Команды для локального запуска Backend:

Создать виртуальное окружение
```
python -m venv venv
```

Активировать виртуальное окружение
```
source venv/Scripts/activate
```

Установить используемые библиотеки
```
pip install -r backend/requirements.txt
```

Выполнить миграции
```
python backend/foodgram/manage.py makemigrations
python backend/foodgram/manage.py migrate
```

Создать суперпользователя
```
python backend/foodgram/manage.py createsuperuser
```

Загрузить список ингридиентов
```
python backend/foodgram/manage.py load_data
```

Подготовить файлы статики
```
python backend/foodgram/manage.py collectstatic --no-input
```

Загрузить локальный сервер
```
python backend/foodgram/manage.py runserver
```
