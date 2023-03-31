--DROP TABLE IF EXISTS encounters;

CREATE TABLE encounters (
	encounter_id TEXT NOT NULL,
	encounter_date date,
	created_at TIMESTAMP DEFAULT NOW()
);