
# Django Marmalade Shop

## Описание проекта

Django Marmalade Shop — это веб-платформа для интернет-магазина, специализирующегося на продаже мармелада и других сладостей. Проект разработан на фреймворке Django и предназначен для удобного управления товарными запасами, заказами и взаимодействия с клиентами.

## Цели проекта
Основная цель проекта — предоставить полнофункциональный интернет-магазин с интуитивно понятным интерфейсом, который обеспечивает высокую скорость работы и удобство при использовании.

### Основные функции:
- **Каталог товаров**: Просмотр товаров, фильтрация по категориям, возможность сортировки и пагинация по каталогу.
- **Корзина покупок**: Пользователи могут добавлять выбранные товары в корзину, изменять количество товара и удалять его из корзины перед оформлением заказа.
- **Оформление заказов**: Поддержка полного цикла заказа от добавления товаров в корзину до подтверждения заказа с возможностью выбора способа оплаты и доставки. Возможность отслеживать состояние заказов.
- **Аутентификация**: Регистрация новых пользователей, аутентификация и управление профилем пользователя, включая историю заказов и настройки аккаунта.
- **Административная панель**: Интерфейс для управления каталогом товаров, заказами и пользователями. Администраторы могут добавлять, удалять или редактировать товары, категории и пользовательские данные.
- **Модели БД**: Связанные базы данных для пользователей/корзин/товаров/категорий.
  

## Технологии
- **Python 3.12**
- **Django 4.2.11**
- **PostgreSQL**
- **HTML**
- **CSS (Bootstrap)**

## Установка и запуск

### Требования
Для запуска проекта вам потребуется Python версии 3.12 и PostgreSQL.

### Шаги для запуска:

1. **Клонирование репозитория**
   ```bash
   git clone https://github.com/mikhailkutuzov0/django-marmalade-shop.git
   cd django-marmalade-shop
   ```

2. **Установка зависимостей**
   ```bash
   pip install -r requirements.txt
   ```

3. **Настройка базы данных PostgreSQL**

   - Установите PostgreSQL и создайте базу данных:
     ```bash
     psql -U postgres
     
     CREATE DATABASE marmalade_shop;
     CREATE USER myuser WITH PASSWORD 'mypassword';
     ALTER ROLE myuser SET client_encoding TO 'utf8';
     ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
     ALTER ROLE myuser SET timezone TO 'UTC';
     GRANT ALL PRIVILEGES ON DATABASE marmalade_shop TO myuser;

     \q

     ```

   - Перейдите в файл `marmalade_shop/settings.py` и настройте подключение к базе данных:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'marmalade_shop',
             'USER': 'myuser',
             'PASSWORD': 'mypassword',
             'HOST': 'localhost',
             'PORT': '',
         }
     }
     ```

4. **Выполнение миграций**
   ```bash
   python manage.py migrate
   python manage.py makemigrations
   ```

5. **Создание суперпользователя**
   ```bash
   python manage.py createsuperuser
   ```

6. **Запуск сервера**
   ```bash
   python manage.py runserver
   ```

   После этих шагов приложение должно быть доступно по адресу `http://127.0.0.1:8000/`.

### Загрузка начальных данных

Для загрузки начальных данных категорий и продуктов в базу данных:

```bash
python manage.py loaddata fixtures/goods/categories.json
python manage.py loaddata fixtures/goods/products.json
```
