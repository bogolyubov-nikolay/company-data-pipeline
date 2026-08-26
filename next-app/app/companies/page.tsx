import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

export default async function CompaniesPage({
  searchParams,
}: {
  searchParams: Promise<{ search?: string; city?: string }>;
}) {
  const params = await searchParams;
  const search = params.search || '';
  const city = params.city || '';

  // Получаем список городов для фильтра
  const citiesResult = await pool.query(
    'SELECT DISTINCT city FROM companies ORDER BY city'
  );
  const cities = citiesResult.rows.map((r) => r.city);

  // Основной запрос с фильтрами
  const companiesResult = await pool.query(
    `SELECT * FROM companies
     WHERE ($1 = '' OR name ILIKE '%' || $1 || '%')
       AND ($2 = '' OR city = $2)
     ORDER BY name
     LIMIT 200`,
    [search, city]
  );
  const companies = companiesResult.rows;

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Компании</h1>

      <form method="GET" style={{ marginBottom: '1rem' }}>
        <input
          type="text"
          name="search"
          placeholder="Поиск по названию"
          defaultValue={search}
        />
        <select name="city" defaultValue={city}>
          <option value="">Все города</option>
          {cities.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
        <button type="submit">Найти</button>
      </form>

      <table border={1} cellPadding={5}>
        <thead>
          <tr>
            <th>Название</th>
            <th>Категория</th>
            <th>Город</th>
            <th>Адрес</th>
            <th>Рейтинг</th>
            <th>Отзывы</th>
            <th>Сайт</th>
            <th>Телефон</th>
          </tr>
        </thead>
        <tbody>
          {companies.map((c) => (
            <tr key={c.id}>
              <td>{c.name}</td>
              <td>{c.category}</td>
              <td>{c.city}</td>
              <td>{c.address}</td>
              <td>{c.rating ?? '—'}</td>
              <td>{c.reviews_count}</td>
              <td>{c.site ? <a href={c.site}>{c.site}</a> : '—'}</td>
              <td>{c.phone ?? '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}