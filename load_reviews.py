import csv
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv('.env.local')

DATABASE_URL = os.getenv("DATABASE_URL")

def main():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS reviews (
        id TEXT,
        name TEXT,
        category TEXT,
        city TEXT,
        address TEXT,
        rating TEXT,
        reviews_count TEXT,
        site TEXT,
        phone TEXT
    );
    """
    cursor.execute(create_table_query)
    print("Таблица reviews создана.")

    with open('data/review.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Прочитано строк в review.csv: {len(rows)}")

    insert_query = """
    INSERT INTO reviews (id, name, category, city, address, rating, reviews_count, site, phone)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    data_to_insert = [(
        row.get('id'),
        row.get('name'),
        row.get('category'),
        row.get('city'),
        row.get('address'),
        row.get('rating'),
        row.get('reviews_count'),
        row.get('site'),
        row.get('phone')
    ) for row in rows]

    try:
        cursor.executemany(insert_query, data_to_insert)
    except Exception as e:
        print(f"Пакетная вставка не удалась ({e}), пробую по одной...")
        for item in data_to_insert:
            cursor.execute(insert_query, item)

    cursor.close()
    conn.close()
    print("Загрузка review.csv завершена.")

if __name__ == "__main__":
    main()
