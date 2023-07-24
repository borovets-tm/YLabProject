# YLab_University
***

## Menu APP 

> Backend: Боровец Тимофей  
> Version: 1.0.0  
> Date: 07/2023

### Процедура развертывания и запуска локального приложения:
1. Скопируйте репозиторий на свою машину:
    `git clone https://github.com/sonic-tim/YLabProject.git`
2. Перейдите в папку проекта:  
    `cd YLabProject`
3. Установите pip и poetry, если они еще не установлен:  
    `pip install --upgrade pip "poetry==1.5.1"`
4. Установите зависимости:  
    `poetry install`
5. Скопируйте содержимое файла `.env.template` в `.env`:  
    `cp .env.template .env`
6. Откройте созданный файл `.env`:  
    `nano .env`
7. Задайте значение для незаполненных параметров:  
    ```
   POSTGRES_USER=<имя пользователя>
   POSTGRES_PASSWORD=<пароль>
   POSTGRES_DB=<название БД>
   ```  
8. Замените значение `HOST_DB` на `localhost`
9. Сохраните и закройте файл сочетанием клавиш в следующем порядке:    
    * **CTRL+O** *(подтвердите сохранение клавишей Enter)*  
    * **CTRL+X**
10. Запустите приложение:  
     `uvicorn menu_app.main:app --reload`

### Процедура развертывания с помощью Docker:
1. Скопируйте репозиторий на свою машину:
    `git clone https://github.com/sonic-tim/YLabProject.git`
2. Перейдите в папку проекта:  
    `cd YLabProject`  
3. Скопируйте содержимое файла `.env.template` в `.env`:  
    `cp .env.template .env`
4. Откройте созданный файл `.env`:  
    `nano .env`
5. Задайте значение для незаполненных параметров:  
    ```
   POSTGRES_USER=<имя пользователя>
   POSTGRES_PASSWORD=<пароль>
   POSTGRES_DB=<название БД>
   ```  
6. Запустите сборку образа и запуск контейнера Docker:  
    `docker compose up --build`

#### После данных манипуляций приложение будет доступно по адресу [localhost:8000](http://localhost:8000/docs) или [127.0.0.1:8000](http://127.0.0.1:8000/docs)
