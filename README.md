# praktikum_new_diplom

### Описание проекта:

Приложение мини социальная сеть по обмену рецептами приготовления
блюд. Backend на фреймворке Django, Frontend на React.

Проект реализован посредством создания 3-х контейнеров Docker и выложен на сервере:
http://jd60.ddns.net     (178.154.226.188)

Данные суперпользователя:    admin@admin.com     Qwerty1234$

### Шаблон наполнения env-файла:

Расположение файла: infra/.env
Данный файл используется для передачи в окружение
приложения следующих переменных без их явного указания в коде:

DB_ENGINE=<тип драйвера БД>
DB_NAME=<имя БД>
POSTGRES_USER=<имя пользователя БД>
POSTGRES_PASSWORD=<пароль пользователя БД>
DB_HOST=<имя хоста БД>
DB_PORT=<порт БД>


### Команды для запуска приложения в контейнерах:

Для управления через docker-compose перейдите в директорию infra:
```
cd infra
```

Создать образы и запустить их контейнеры:
```
sudo docker-compose up
```

Миграции для моделей и сбор статики создаются на этапе сборки контейнера backend.

Применить миграции в БД:
```
sudo docker-compose exec backend python3 manage.py migrate
```


Создать суперпользователя в БД для администрирования:
```
sudo docker-compose exec backend python3 manage.py createsuperuser
```

Загрузить предустановленную таблицу ингредиентов:
```
sudo docker-compose exec backend python3 manage.py load_data
```

### Команда для заполнения базы тестовыми данными(перед выполнение очистить БД):

```
sudo docker-compose exec backend python3 manage.py loaddata fixtures.json
```

### Файл с тестовыми данными в репозиторий не входит, он может быть снят с заполненной базы данных командой:
```
sudo docker-compose exec backend python3 manage.py dumpdata > fixtures.json
```



