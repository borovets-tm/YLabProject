# YLab_University
***
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
## Menu APP

> Backend: Боровец Тимофей
> Version: 1.0.0
> Date: 07/2023

### Процедура развертывания и запуска локального приложения:
1. Скопируйте репозиторий на свою машину:
    ```shell
   git clone https://github.com/sonic-tim/YLabProject.git
    ```
2. Перейдите в папку проекта:
    ```shell
   cd YLabProject
    ```
3. Установите виртуальное окружение:
    ```shell
    python -m venv venv
    ```
4. Активируйте виртуальное окружение:
    ```shell
    source venv/bin/activate
    ```
5. Установите pip если они еще не установлен:
    ```shell
    python -m pip install --upgrade pip
    ```
6. Установите poetry:
    ```shell
    pip install poetry
    ```
7. Установите зависимости:
    ```shell
    poetry install
    ```
8. Скопируйте содержимое файла `.env.template` в `.env`:
    ```shell
    cp .env.template .env
    ```
9. Откройте созданный файл `.env`:
    ```shell
    nano .env
    ```
10. Задайте значение для незаполненных параметров:
     ```
    POSTGRES_USER=<имя пользователя>
    POSTGRES_PASSWORD=<пароль>
    POSTGRES_DB=<название БД>
    TEST_DB=<название тестовой БД>
    ```
11. Замените значение `HOST_DB`, `TEST_HOST_DB` и `REDIS_HOST` на `localhost`
#### Параметры указываются из расчета, что PostgreSQL установлен на локальной машине в противном случае используйте собственные параметры для подключения!
12. Сохраните и закройте файл сочетанием клавиш в следующем порядке:
     * **CTRL+O** *(подтвердите сохранение клавишей Enter)*
     * **CTRL+X**
13. Запустите приложение:
     ```shell
    uvicorn menu_app.main:app --reload
    ```
***
### Процедура развертывания с помощью Docker:
1. Скопируйте репозиторий на свою машину:
    ```shell
    git clone https://github.com/sonic-tim/YLabProject.git
    ```
2. Перейдите в папку проекта:
    ```shell
    cd YLabProject
    ```
3. Скопируйте содержимое файла `.env.template` в `.env`:
    ```shell
   cp .env.template .env
   ```
4. Откройте созданный файл `.env`:
    ```shell
   nano .env
   ```
5. Задайте значение для незаполненных параметров:
    ```
   POSTGRES_USER=<имя пользователя>
   POSTGRES_PASSWORD=<пароль>
   POSTGRES_DB=<название БД>
   TEST_DB=<название тестовой БД>
   ```
6. Запустите сборку образа и запуск контейнера Docker:
    ```shell
   docker-compose up -d
   ```

#### После данных манипуляций приложение будет доступно по адресу [localhost:8000](http://localhost:8000/docs) или [127.0.0.1:8000](http://127.0.0.1:8000/docs)
***
## Запуск тестов приложения
1. Для запуска тестов используйте инструкцию "Процедура развертывания с помощью
Docker", заменив пункт 6 на команду ниже:
    ```shell
    docker-compose -f test.docker-compose.yaml up --attach test --abort-on-container-exit && docker-compose -f test.docker-compose.yaml down
    ```
    > При выполнении данной команды, будет запущен тестовый сценарий, который
    > развернет и запустит pytest, выведет в консоль информацию о результатах
    > тестов, после чего остановит и удалит контейнеры.

**Если перед запуском тестов выполнялось развертывание приложения с помощью
Docker, то для запуска теста достаточно выполнить команду запуска.**
