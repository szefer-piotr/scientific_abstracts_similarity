CREATE TABLE search_results (
  id SERIAL PRIMARY KEY,
  timestamp TIMESTAMP default CURRENT_TIMESTAMP,
  query TEXT NOT NULL,
  items TEXT NOT NULL
);