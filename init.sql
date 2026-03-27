CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255),
    password VARCHAR(255),
    location_id VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS user_roles (
    user_id VARCHAR(255) PRIMARY KEY,
    role VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS events (
    event_id VARCHAR(255) PRIMARY KEY, -- python UUID hex
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    capacity INT,
    booked INT, -- number of seats book < capacity
    start DATETIME,
    end DATETIME,
    location_id VARCHAR(255), -- python UUID hex
    category VARCHAR(255),
    price DECIMAL(10, 2),
    currency VARCHAR(10) -- Pydantic Currency
);

CREATE TABLE IF NOT EXISTS bookings (
    booking_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    event_id VARCHAR(255),
    seats INT,
    total_price DECIMAL(10, 2),
    currency VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS locations (
    location_id VARCHAR(255) PRIMARY KEY,
    country VARCHAR(255),
    city VARCHAR(255),
    timezone VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    balance DECIMAL(10, 2),
    currency VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(255) PRIMARY KEY,
    booking_id VARCHAR(255),
    account_id VARCHAR(255),
    amount DECIMAL(10, 2),
    currency VARCHAR(10)
);
