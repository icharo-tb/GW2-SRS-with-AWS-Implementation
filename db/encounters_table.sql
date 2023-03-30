-- DROP TABLE IF EXISTS encounter_table;

CREATE TABLE encounters (
	encounter_id UUID PRIMARY KEY UNIQUE,
	encounter_date date,
	created_at TIMESTAMP DEFAULT NOW()
);