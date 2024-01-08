CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    hash TEXT NOT NULL,
);
CREATE UNIQUE INDEX users_email ON users(email);

CREATE TABLE transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    ammount INTEGER INTEGER NOT NULL,
    date TEXT NOT NULL,
    currency TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES transaction_categories(id)
);
CREATE INDEX transactions_user_id ON transactions(user_id);
CREATE INDEX transactions_category_id ON transactions(category_id);

CREATE TABLE transaction_categories(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE INDEX transaction_categories_user_id ON transaction_categories(user_id);
CREATE INDEX transaction_categories_type ON transaction_categories(type);

CREATE TABLE exchanges(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    source_currency TEXT NOT NULL,
    source_ammount INTEGER NOT NULL,
    destination_currency TEXT NOT NULL,
    destination_ammount INTEGER NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE INDEX exchanges_source_currency ON exchanges(source_currency);
CREATE INDEX exchanges_destination_currency ON exchanges(destination_currency);
CREATE INDEX exchanges_user_id ON exchanges(user_id);

-- Refers to how much 1 USD is worth in the currency each column refers to
CREATE TABLE historical_rates(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    brl INTEGER,
    eur INTEGER,
    gbp INTEGER
);
CREATE UNIQUE INDEX historical_rates_date ON historical_rates(date);