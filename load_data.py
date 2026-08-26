import json
import os
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

load_dotenv('.env.local')

DATABASE_URL = os.getenv("DATABASE_URL")

DATA_DIR = Path(__file__).parent / 'data'

def read_json_files(directory: Path):
    records = []
    for file_path in sorted(directory.glob('page_*.json')):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            records.extend(data.get('items', []))
    return records

def deduplicate(records):
    unique = {}
    for rec in records:
        unique[rec['id']] = rec
    return list(unique.values())

def main():
    print("Читаю JSON файлы...")
    records = read_json_files(DATA_DIR)
    print(f"Всего записей до дедупликации: {len(records)}")

    unique_records = deduplicate(records)
    print(f"Уникальных записей после дедупликации: {len(unique_records)}")

    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS companies (
        id VARCHAR(20) PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        city TEXT,
        address TEXT,
        rating NUMERIC(3,1),
        reviews_count INTEGER DEFAULT 0,
        site TEXT,
        phone TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_companies_city ON companies(city);
    CREATE INDEX IF NOT EXISTS idx_companies_category ON companies(category);
    CREATE INDEX IF NOT EXISTS idx_companies_name ON companies(name);
    """
    cursor.execute(create_table_query)
    print("Таблица companies создана.")

    insert_query = """
    INSERT INTO companies (id, name, category, city, address, rating, reviews_count, site, phone)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO UPDATE SET
        name = EXCLUDED.name,
        category = EXCLUDED.category,
        city = EXCLUDED.city,
        address = EXCLUDED.address,
        rating = EXCLUDED.rating,
        reviews_count = EXCLUDED.reviews_count,
        site = EXCLUDED.site,
        phone = EXCLUDED.phone;
    """

    data_to_insert = []
    for rec in unique_records:
        rating = rec.get('rating')
        if rating is not None:
            try:
                rating = float(rating)
            except (TypeError, ValueError):
                rating = None

        reviews_count = rec.get('reviews_count')
        if reviews_count is not None:
            try:
                reviews_count = int(reviews_count)
            except (TypeError, ValueError):
                reviews_count = 0

        data_to_insert.append((
            rec['id'],
            rec.get('name'),
            rec.get('category'),
            rec.get('city'),
            rec.get('address'),
            rating,
            reviews_count,
            rec.get('site'),
            rec.get('phone')
        ))

    print("Загружаю данные в PostgreSQL...")
    try:
        cursor.executemany(insert_query, data_to_insert)
    except Exception as e:
        print(f"Пакетная вставка не удалась ({e}), пробую по одной...")
        for item in data_to_insert:
            cursor.execute(insert_query, item)

    cursor.close()
    conn.close()
    print("Загрузка завершена успешно!")

if __name__ == "__main__":
    main()
