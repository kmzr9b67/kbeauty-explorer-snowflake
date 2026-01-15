-- 1. CLEANUP
-- Drop tables in reverse order of creation to avoid 
-- Foreign Key constraint errors.
DROP TABLE IF EXISTS PRODUCTS;
DROP TABLE IF EXISTS SKIN_TYPES;
DROP TABLE IF EXISTS CONCERNS;
DROP TABLE IF EXISTS AGE_RANGES;
DROP TABLE IF EXISTS ROUTINE_STEPS;

-- 2. CREATE LOOKUP TABLES (Dictionaries)

-- Table for skin categories (e.g., Dry, Oily) and expert advice
CREATE TABLE SKIN_TYPES (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    advice VARCHAR(255)
);

-- Table for specific skin issues (e.g., Acne, Brightening)
CREATE TABLE CONCERNS (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Table for user age brackets
CREATE TABLE AGE_RANGES (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE
);

-- Table for the steps in the skincare routine (defines display order)
CREATE TABLE ROUTINE_STEPS (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    sequence INT NOT NULL
);

-- 3. CREATE MAIN TABLE (Fact Table)

-- The core table connecting all dictionaries into specific recommendations
CREATE TABLE PRODUCTS (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    brand VARCHAR(100),
    rating FLOAT,
    skin_type_id INT,
    concern_id INT,
    age_range_id INT,
    step_id INT,
    -- Establishing relationships with lookup tables
    FOREIGN KEY (skin_type_id) REFERENCES SKIN_TYPES(id),
    FOREIGN KEY (concern_id) REFERENCES CONCERNS(id),
    FOREIGN KEY (age_range_id) REFERENCES AGE_RANGES(id),
    FOREIGN KEY (step_id) REFERENCES ROUTINE_STEPS(id)
);