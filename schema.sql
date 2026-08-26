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