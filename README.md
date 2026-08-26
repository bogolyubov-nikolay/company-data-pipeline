# Обработка данных и каталог компаний

Проект демонстрирует полный цикл работы с данными: от разбора JSON-выгрузки до интерактивного веб-интерфейса.

## Возможности
- Загрузка 1000+ записей о компаниях из JSON в PostgreSQL (дедупликация, индексы)
- Три аналитических SQL-запроса
- Веб-страница на Next.js с поиском по названию и фильтром по городу
- Отчёт о качестве данных (`ANOMALIES.md`) и описание проверки (`CHECK.md`)

## Технологии
- Python (psycopg2)
- PostgreSQL (Supabase)
- SQL
- Next.js (App Router, TypeScript)
- Git / GitHub

## Как запустить

1. Установите зависимости Python:
   pip install psycopg2-binary python-dotenv

2. В корне проекта создайте файл .env.local и укажите строку подключения к PostgreSQL (Supabase):
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@your-db.supabase.co:5432/postgres

3. Загрузите данные:
   python load_data.py
   python load_reviews.py

4. Перейдите в папку next-app:
   cd next-app

5. Внутри next-app тоже создайте файл .env.local с той же строкой подключения.

6. Установите зависимости и запустите приложение:
   npm install
   npm run dev

7. Откройте http://localhost:3000/companies

## Скриншоты

### Веб-страница
![Все компании](companies-page-all.jfif)
![Поиск по названию](companies-page-search.jfif)
![Фильтр по городу](companies-page-filter.jfif)

### SQL-запросы
![Топ-5 категорий](sql-top-categories.jfif)
![Средний рейтинг по городам](sql-avg-rating.jfif)
![Доля компаний с сайтом](sql-site-share.jfif)

## Автор

Николай Боголюбов  
Email: bnikolai82@mail.ru  
Telegram: [@bogolyubov_n](https://t.me/bogolyubov_n)
