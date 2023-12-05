DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS inproceedings;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT UNIQUE,
	password TEXT
);

CREATE TABLE inproceedings (
	id SERIAL PRIMARY KEY,
	cite_id TEXT,
	author TEXT,
	title TEXT,
	year INTEGER,
	booktitle TEXT,
	start_page INTEGER,
	end_page INTEGER,
	user_id INTEGER REFERENCES users
);

CREATE TABLE articles (
	id SERIAL PRIMARY KEY,
	cite_id TEXT,
	author TEXT,
	title TEXT,
	journal TEXT,
	year INTEGER,
	volume INTEGER,
	start_page INTEGER,
	end_page INTEGER,
	user_id INTEGER REFERENCES users
);

CREATE TABLE books (
	id SERIAL PRIMARY KEY,
	cite_id TEXT,
	author TEXT,
	title TEXT,
	year INTEGER,
	publisher TEXT,
	start_page INTEGER,
	end_page INTEGER,
	user_id INTEGER REFERENCES users
);
