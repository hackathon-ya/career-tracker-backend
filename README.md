# **Конкурс «Хакатон Резюме.Разработка»**

### Организатор: АНО ДПО «Образовательные технологии Яндекса»

## Бэкенд модуля "Карьерный трекер"

### Команда № 9 "Dream Team"

Разработчики: [Ушаков Дмитрий](https://github.com/Voyager1744), [Михаил Францкевич](https://github.com/OGURETS13)

На время конкурса проект будет доступен по адресу: http://158.160.53.161

Административная панель: логин: admin, пароль: admin

Стэк технологий: Python, Django, DRF

### Документация API
В проекте реализована автоматическая генерация документации. Документация доступна по адресам:
1) Swagger: `/api/v1/schema/swagger-ui/`
2) Redoc: `/api/v1/schema/redoc/`


## Запуск в режиме разработки

1. Убедитесь, что у вас установлены Docker и Docker Compose.

2. Склонируйте данный репозиторий на свой локальный компьютер:

   ```bash
   git clone git@github.com:hackathon-ya/career-tracker-backend.git
   ```

3. Перейдите в директорию с проектом:
   ```bash
   cd career-tracker-backend
   ```
   
4. Создайте файл .env в корне проекта с переменными окружения
   и скопируйте в него данные из файла ".env.example":

   ```bash
   touch .env
   ```
   В приведенном примере .env файла:

   ```bash
         # Параметры Django
         DJANGO_SUPERUSER_PASSWORD # Пароль для суперпользователя Django, который будет создан при инициализации приложения.
         DJANGO_SECRET_KEY # Секретный ключ Django, используемый для хэширования паролей, создания токенов и других целей безопасности.

         # Параметры для подключения к базе данных PostgreSQL.
         POSTGRES_DB # имя БД
         POSTGRES_USER # имя пользователя БД
         POSTGRES_PASSWORD # пароль пользователя БД
         POSTGRES_HOST # хост, на котором развернута БД
         POSTGRES_PORT # порт, на котором развернута БД
      ```
5. Соберите Docker-образы и запустите контейнеры:

   ```bash
   docker-compose -f docker-compose.dev.yaml build
   ```

   ```bash
   docker-compose -f docker-compose.dev.yaml up -d
   ```
6. После успешного запуска, Django приложение будет
доступно по адресу http://localhost:8000/.

7. Чтобы создать superuser, выполните команду:
   ```
   docker exec -it careertracker_backend python manage.py createsuperuser
   ```
8. Вы можете остановить контейнеры с помощью команды:

   ```bash
   docker-compose -f docker-compose.dev.yaml down
   ```

пример файла .env

```
# django
DJANGO_SUPERUSER_PASSWORD=mysecretpassword
DJANGO_SECRET_KEY=mysecretkey

# postgres
POSTGRES_DB=careertracker
POSTGRES_USER=careertracker
POSTGRES_PASSWORD=mypassword
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
```
