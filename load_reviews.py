import csv
import psycopg2

# Строка подключения (та же, что для load_data.py)
DATABASE_URL = "postgresql://postgres.swgutpssbzkjzehtoqtx:nzjSDGZzxFTxqc0u@aws-0-eu-central-1.pooler.supabase.com:5432/postgres"

def main():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Создаём таблицу reviews с текстовыми полями, чтобы принять все аномалии
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
    conn.commit()
    print("Таблица reviews создана.")

    # Читаем review.csv
    with open('review.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Прочитано строк в review.csv: {len(rows)}")

    insert_query = """
    INSERT INTO reviews (id, name, category, city, address, rating, reviews_count, site, phone)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for row in rows:
        cursor.execute(insert_query, (
            row.get('id'),
            row.get('name'),
            row.get('category'),
            row.get('city'),
            row.get('address'),
            row.get('rating'),
            row.get('reviews_count'),
            row.get('site'),
            row.get('phone')
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("Загрузка review.csv завершена.")

if __name__ == "__main__":
    main()