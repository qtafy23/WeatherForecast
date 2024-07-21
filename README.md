# **WeatherForecast**


## **Содержание**

* #### Инструкция по запуску проекта
* #### Выполненные задачи на данный момент
* #### Технологии


### **Инструкция по запуску проекта**


#### Клонировать репозиторий и перейти в директорию проекта:

```
git clone git@github.com:qtafy23/WeatherForecast.git

cd WeatherForecast/
```

#### Создать вирутальное окружение и установить зависимости

```
python -m venv venv

source venv/scripts/activate

pip install -r requirements.txt
```

##### Перейти в директорию config и заполнить файл .secrets.toml

```
cd config/

cp .secrets.example.toml .secrets.toml
```

#### Создать миграции и запустить сервер!

```
python manage.py makemigrations

python manage.py migrate

python manage.py runserver
```


### **Выполненные задачи на данный момент**


1. [ ] Минимальное покрытие тестами
2. [ ] Проект помещен в докер контейнер
3. [x] Сделаны автодополнение (подсказки) при вводе города
4. [x] При повторном посещении сайта будет предложено посмотреть погоду в городе, в котором пользователь уже смотрел ранее
5. [ ] Сохраняется история поиска для каждого пользователя, и будет API, показывающее сколько раз вводили какой город
6. [x] web приложение, оно же сайт, где пользователь вводит название города, и получает прогноз погоды в этом городе на ближайшее время.


### **Технологии**


```
Django 4.2.14
Django REST Framework 3.14.0
```