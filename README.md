# YLab_University
***
![FastAPI](https://a11ybadges.com/badge?logo=fastapi)
![Python](https://a11ybadges.com/badge?logo=python)
![PostgreSQL](https://a11ybadges.com/badge?logo=postgresql)
![Docker](https://a11ybadges.com/badge?logo=docker)
![Redis](https://a11ybadges.com/badge?logo=redis)
![RabbitMQ](https://a11ybadges.com/badge?logo=rabbitmq)
![Celery](https://a11ybadges.com/badge?logo=celery)
## Menu APP

> Backend: Боровец Тимофей
> Version: 1.0.0
> Date: 07/2023
***
### Приложение разворачивается с помощью Docker по следующей схеме:
1. Установите Docker на Вашу машину по инструкции из [Docker docs](https://docs.docker.com/desktop/)
2. Скопируйте репозиторий на свою машину:
    ```shell
    git clone https://github.com/sonic-tim/YLabProject.git
    ```
3. Перейдите в папку проекта:
    ```shell
    cd YLabProject
    ```
4. Скопируйте содержимое файла `.env.template` в `.env`:
    ```shell
   cp .env.template .env
   ```
5. Откройте созданный файл `.env`:
    ```shell
   nano .env
   ```
6. Задайте значение для незаполненных параметров:
    ```
   POSTGRES_USER=<имя пользователя>
   POSTGRES_PASSWORD=<пароль>
   POSTGRES_DB=<название БД>
   TEST_DB=<название тестовой БД>
   RABBITMQ_DEFAULT_USER=<имя пользователя для MQRabbit>
   RABBITMQ_DEFAULT_PASS=<пароль для MQRabbit>
   ```
7. Запустите сборку образа и запуск контейнера Docker:
    ```shell
   docker-compose up -d
   ```
***
> **ВНИМАНИЕ!** Тесты из Postman могут не проходить, если в Базе данных есть
> записи. Для прохождения тестов вместо команды из п.7. Введите команду:
> ```shell
> docker-compose up -d app db redis
> ```
> После тестирования повторите ввод команды из п.7 - незапущенные службы будут
> запущены
***
#### После данных манипуляций приложение будет доступно по адресу [localhost:8000](http://localhost:8000/docs) или [127.0.0.1:8000](http://127.0.0.1:8000/docs)
***
> **ВНИМАНИЕ!** Фоновая задача по обновлению данных из excel таблицы запустится
> не раньше, чем через 15 секунд после запуска контейнеров! Это связано с механизмом
> запуска RabbitMQ.
***
## Запуск тестов приложения
1. Для запуска тестов используйте инструкцию "Процедура развертывания с помощью
Docker", заменив пункт 6 на команду ниже:
    > **ВНИМАНИЕ!** Если до тестирования производилось развертывание основного
   > приложения, то достаточно только ввести данную команду.

    ```shell
    docker-compose -f test.docker-compose.yaml up --attach test --abort-on-container-exit && docker-compose -f test.docker-compose.yaml down
    ```
   > При выполнении данной команды, будет запущен тестовый сценарий, который
   > развернет и запустит pytest, выведет в консоль информацию о результатах
   > тестов, после чего остановит и удалит контейнеры.
#### Список тестов
* `tests/unit/test_app.py` - тестирование получения древовидного меню.
* `tests/unit/test_count_from_postman.py` - тестирование количества меню/подменю/блюд из Postman.
* `tests/unit/test_crud_dish.py` - тестирование CRUD для Блюд.
* `tests/unit/test_crud_menu.py` - тестирование CRUD для Меню.
* `tests/unit/test_crud_submenu.py` - тестирование CRUD Под-меню.
* `tests/unit/test_healthcheck.py` - завершение тестов(удаление БД и кэша).

***
## Ключевые моменты
* Тесты написаны только для "ручек".
* Фоновая задача обновляет данные меню каждые 15 секунд. На текущий момент
   время жизни кэша составляет также 15 секунд.
* **ВАЖНО!** В файле Menu.xlsx разделителем дробной части цен является точка.

## Реализации со звездочкой
* Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM запрос.
   > Данная реализация расположена в menu_app.repositories.menu_repository.MenuRepository.get_list
* Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest
   > Данная реализация расположена в tests/unit/test_count_from_postman.py
* Описать ручки API в соответствий c OpenAPI
   > Данная реализация расположена в menu_app/routers
* Реализовать в тестах аналог Django reverse() для FastAPI
   > Данная реализация расположена в tests.unit.config_test.config_base.TestReverseClient.reverse
* Обновление меню из google sheets раз в 15 сек.
    > В процессе реализации.
* Блюда по акции. Размер скидки (%) указывается в столбце G файла Menu.xlsx
    > Данная реализация расположена в:
  > * menu_app.models.Dish.current_price - модель;
  > * menu_app.repositories.dish_repository.DishRepository.get_list - пример запроса
  > * menu_app.tasks.update_db_from_excel - обработчик
***
> ВАЖНО! По непонятной пока причине, изменение файла из системы пока не отражается
> на файле в Docker контейнере. Поиск решения проблемы продолжается. На текущий момент
> решением является перезапуск контейнеров.
