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

INSERT INTO users (user_id, username, firstname, lastname, password, location_id)
VALUES ('fb853938b2104b58bb47fd38cf35eafc', 'admin', 'Admin', NULL, '$2b$12$6R9tNqFY6aeFKf5UwkhjlOkmctGkPn2V3vlHnec3hpNWQVe.jIROq', NULL);

INSERT INTO events (event_id, name, description, capacity, booked, start, end, location_id, category, price, currency)
VALUES
('0280298dc1a84580b14471731f9efdc7', 'Business Workshop 2026', 'An exciting workshop about industry trends.', 373, 50, '2026-05-18 16:00:00', '2026-05-18 18:00:00', NULL, 'Conference', 33.20, 'GBP'),
('25a7ff1519ca4eed92875b45a53dc11f', 'Global Tech Conference', 'Annual gathering for software engineers.', 449, 365, '2026-05-23 09:00:00', '2026-05-23 17:00:00', NULL, 'Conference', 60.25, 'USD'),
('982a82f9a7704d64811c4edc3201b2cb', 'Jazz Night in the Park', 'Outdoor evening concert with local artists.', 167, 132, '2026-05-27 18:00:00', '2026-05-27 23:00:00', NULL, 'Music', 26.71, 'USD'),
('8b28c08fba594b8d986b1b4e9a5c2038', 'Creative Networking Meetup', 'Mixer for designers and illustrators.', 418, 120, '2026-05-14 12:00:00', '2026-05-14 14:00:00', NULL, 'Conference', 28.43, 'USD'),
('e398716382904c9bb4e92976f6277943', 'Cybersecurity Summit', 'Protecting assets in the digital age.', 500, 412, '2026-06-15 09:00:00', '2026-06-16 17:00:00', NULL, 'Conference', 120.00, 'USD'),
('d9e8f7a6b5c443218d7e6f5a4b3c2d1e', 'Sunset Rooftop DJ Set', 'Deep house music at the Sky Lounge.', 150, 149, '2026-07-04 18:00:00', '2026-07-05 01:00:00', NULL, 'Music', 45.00, 'USD'),
('8a96245e4c04435590cab9621bf51960', 'Neon Horizon', 'Electronica and light show experience.', 17299, 15818, '2026-07-18 00:00:00', '2026-07-20 00:00:00', NULL, 'Music', 153.38, 'GBP'),
('1b292b95476e4bbe9ee7112477d38df3', 'Acoustic Roots', 'Folk and acoustic music in the woods.', 32507, 23699, '2026-07-06 00:00:00', '2026-07-09 00:00:00', NULL, 'Music', 218.33, 'GBP'),
('be4a0603d9154066a3fe8ecea6fed5e4', 'Velocity Metal Fest', 'High-energy metal and hard rock.', 6582, 4215, '2026-08-24 00:00:00', '2026-08-27 00:00:00', NULL, 'Music', 205.12, 'EUR'),
('96113ecee4d14668aea2a6a88f37bac4', 'Solstice Jazz', 'Celebrating jazz under the midnight sun.', 47680, 35506, '2026-07-03 00:00:00', '2026-07-05 00:00:00', NULL, 'Music', 194.12, 'EUR'),
('cd4d05376de644bb8f79e280a3315cb9', 'Urban Beats', 'Hip-hop and street culture festival.', 5655, 4941, '2026-07-07 00:00:00', '2026-07-09 00:00:00', NULL, 'Music', 367.37, 'USD'),
('f716da09d3ee407ab4892dd30178e37b', 'Classic Harmony', 'A weekend of symphonic masterpieces.', 40856, 33970, '2026-08-04 00:00:00', '2026-08-06 00:00:00', NULL, 'Music', 261.35, 'USD'),
('2e6478bf61204868a15221d26f567a03', 'Desert Mirage', 'Alternative indie bands in the dunes.', 45160, 33910, '2026-08-24 00:00:00', '2026-08-26 00:00:00', NULL, 'Music', 212.06, 'GBP'),
('24ef902c96ac4b63b4506b072e3182d1', 'Rhythm & Blues Gala', 'Soulful performances by legendary artists.', 47291, 36245, '2026-08-10 00:00:00', '2026-08-13 00:00:00', NULL, 'Music', 386.23, 'USD');
