# YLab_University

## Menu APP 

> Backend: Боровец Тимофей  
> Version: 1.0.0  
> Date: 07/2023

### Процедура развертывания и запуска приложения:
1. Установите pip и poetry, если они еще не установлен:  
    `pip install --upgrade pip "poetry==1.5.1"`
2. Установите зависимости:  
    `poetry install`
3. Скопировать содержимое файла `.env.template` в `.env`:  
    `cp .env.template .env`
4. Откройте созданный файл `.env`:  
    `nano .env`
5. Задайте значение для *SQLALCHEMY_URL* в виде строки с адресом к БД:  
    `SQLALCHEMY_URL='<addres_to_db>'`
6. Сохраните и закройте файл сочетанием клавиш в следующем порядке:    
    * **CTRL+O** *(подтвердите сохранение клавишей Enter)*  
    * **CTRL+X**
7. Запустите приложение:  
    `uvicorn menu_app.main:app --reload`

#### После данных манипуляций приложение будет доступно по адресу [localhost:8000](http://localhost:8000/docs) или [127.0.0.1:8000](http://127.0.0.1:8000/docs)
