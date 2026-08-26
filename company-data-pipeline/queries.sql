-- 1. Топ-5 категорий по числу компаний
SELECT category, COUNT(*) AS company_count
FROM companies
GROUP BY category
ORDER BY company_count DESC
LIMIT 5;

-- 2. Средний рейтинг по городам среди компаний с 10+ отзывами
SELECT city, AVG(rating) AS avg_rating
FROM companies
WHERE reviews_count >= 10 AND rating IS NOT NULL
GROUP BY city
ORDER BY avg_rating DESC;

-- 3. Доля компаний с сайтом по категориям
SELECT category,
       COUNT(*) AS total,
       SUM(CASE WHEN site IS NOT NULL AND site != '' THEN 1 ELSE 0 END) AS with_site,
       ROUND(100.0 * SUM(CASE WHEN site IS NOT NULL AND site != '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS site_percentage
FROM companies
GROUP BY category
ORDER BY site_percentage DESC;