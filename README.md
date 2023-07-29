# YLab_University
***

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
    pip "poetry==1.5.1"
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
    ```  
11. Замените значение `HOST_DB` на `localhost`
#### Параметры указываются из расчета, что PostgreSQL установлен на локальной машине в противном случае используйте собственные параметры для подключения!
12. Сохраните и закройте файл сочетанием клавиш в следующем порядке:    
     * **CTRL+O** *(подтвердите сохранение клавишей Enter)*  
     * **CTRL+X**
13. Запустите приложение:  
     ```shell
    uvicorn menu_app.main:app --reload
    ```

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
   ```  
6. Запустите сборку образа и запуск контейнера Docker:  
    ```shell
   docker-compose up -d
   ```

#### После данных манипуляций приложение будет доступно по адресу [localhost:8000](http://localhost:8000/docs) или [127.0.0.1:8000](http://127.0.0.1:8000/docs)
