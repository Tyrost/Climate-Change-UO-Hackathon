-- Create the database
CREATE DATABASE SubscribersDB;

-- Select the database
USE SubscribersDB;

-- Create the subscribers table
CREATE TABLE subscribers (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID for each subscriber
    name VARCHAR(100) NOT NULL,         -- Subscriber's name
    email VARCHAR(100) NOT NULL UNIQUE, -- Subscriber's email (unique)
);