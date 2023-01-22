# Тестовое задание


>Технологии, используемые на проекте:

>>1. Python ![Python](https://img.shields.io/badge/-Python-black?style=flat-square&logo=Python)
>>2. Django ![Django](https://img.shields.io/badge/-Django-0aad48?style=flat-square&logo=Django)
>>3. DjangoRestFramework ![Django Rest Framework](https://img.shields.io/badge/DRF-red?style=flat-square&logo=Django)
>>4. PostgresSQL ![Postgresql](https://img.shields.io/badge/-Postgresql-%232c3e50?style=flat-square&logo=Postgresql)
>>5. Nginx ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=flat-square&logo=nginx&logoColor=white)
>>6. Swagger ![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=flat-square&logo=swagger&logoColor=white)

# Как запустить проект:

В папку ***infra*** расположить .env файл со следующими параметрами:
1. DJANGO_SECRET_KEY=***ВАШ СЕКРЕТНЫЙ КЛЮЧ ПРОЕКТА***
2. DJANGO_DEBUG=***Уровень дебага проекта***
3. DJANGO_LOG_LEVEL=**Уровень логирования проекта***
4. POSTGRES_USER=***ВАШЕ ИМЯ ПОЛЬЗОВАТЕЛЯ ОТ БД***
5. POSTGRES_PASSWORD=***ВАШ ПАРОЛЬ ОТ БД***
6. POSTGRES_DB=***ИМЯ БАЗЫ ДАННЫХ***
7. POSTGRES_HOST=***ХОСТ, УКАЗАТЬ СЛУЖБУ БД,В НАШЕМ СЛУЧАЕ postgresql_db***
8. POSTGRES_PORT=***Порт базы данный***

Скачать docker: 
1. Для [windows](https://docs.docker.com/desktop/windows/install/)
2. Для [macOS](https://docs.docker.com/desktop/mac/install/)
3. Для дистрибутивов [Linux](https://docs.docker.com/desktop/linux/#uninstall)

После установки проверьте конфигурацию переменных окружений 
командой:
```
docker-compose config
```
Если всё успешно, все переменные на местах, запустить командой:
```
docker-compose -f production.yml up --build
```
Что бы создать суперпользователя, 
необходимо войти в контейнер командой:
```
docker exec -it drf_server bash
```
После ввести команду:
```
python manage.py createsuperuser
```
и следовать дальнейшим инструкциям.

Для выхода введите:
```
exit
```
Следующие сервисы будут доступны по адресам:

## API
1. http://localhost:8000/api/swagger/
