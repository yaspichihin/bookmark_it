# Версия python 
```txt
Python 3.12.3
Docker version 27.0.2, build 912c1dd
Docker Compose version v2.28.1
```

# INSTALL

Установка виртуального окружения
```shell
python -m venv .venv
```
Применение виртуального окружения
```shell
source .venv/bin/activate
```
Установка зависимостей
```shell
pip install -r requirements.txt
```
Запуск Redis
```shell
docker compose up -d
```

# Настройка

Проверим миграции и применим их к БД
```shell
python bookmarks/manage.py makemigrations
python bookmarks/manage.py migrate
```

Создайте запись супер пользователя.
```sheel
python bookmarks/manage.py createsuperuser
```


Добавить в .env:
* GOOGLE_OAUTH2_KEY
* GOOGLE_OAUTH2_SECRET
* REDIS_HOST
* REDIS_PORT
* REDIS_DB
* SECRET_KEY

Добавьте локальную запись `mysite.com`, которая доступна на 127.0.0.1. \
Это важно для работы HTTPS, OAUTH и кнопки `BOOKMART IT`.\
Кнопка содержит JS код c ссылкой на `mysite.com` для встраивания окна на других сайтах.
```shell
$ cat /etc/hosts | grep mysite
127.0.0.1 mysite.com
```



# Запуск сервера в режиме HTTPS
```shell
python bookmarks/manage.py runserver_plus --cert-file cert.crt
```

Перейдите в браузере на страницу приложения.
```txt
https://mysite.com:8000/account/login/
```

Для администрирования данных через админ панель. \
Использовать учетную запись суперпользователя.
```txt
https://mysite.com:8000/admin/
```