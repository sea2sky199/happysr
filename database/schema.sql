CREATE DATABASE IF NOT EXISTS happysr CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE happysr;

CREATE TABLE IF NOT EXISTS sr_users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('user','admin') DEFAULT 'user',
  name VARCHAR(100),
  gender ENUM('male','female','other','prefer_not_to_say'),
  age INT,
  zipcode VARCHAR(10),
  language_pref VARCHAR(5) DEFAULT 'en',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sr_activities (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  location VARCHAR(255),
  event_date DATETIME NOT NULL,
  category VARCHAR(50),
  created_by INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by) REFERENCES sr_users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS sr_expenses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  category VARCHAR(50),
  description VARCHAR(255),
  expense_date DATE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES sr_users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sr_investments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  type VARCHAR(50),
  institution VARCHAR(100),
  amount DECIMAL(12,2),
  notes TEXT,
  as_of_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES sr_users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sr_calendar_events (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  event_date DATE NOT NULL,
  is_public BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
