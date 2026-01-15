-- POPULATING LOOKUP TABLES (App Filters)

-- Define skin types and the advice shown in the app
INSERT INTO SKIN_TYPES (name, advice) VALUES 
('Dry', 'Focus on hydration and oil-based products.'),
('Oily', 'Use lightweight, non-comedogenic formulas.'),
('Combination', 'Balance hydration for cheeks and sebum control for T-zone.'),
('Sensitive', 'Avoid fragrance and harsh active ingredients.');

-- Define primary skin concerns
INSERT INTO CONCERNS (name) VALUES 
('Acne'), ('Aging'), ('Hydration'), ('Brightening'), ('Redness');

-- Define age ranges for the quiz
INSERT INTO AGE_RANGES (name) VALUES 
('<20'), ('20-30'), ('30-40'), ('40-50'), ('50+');

-- Define the 5-step Korean skincare routine sequence
INSERT INTO ROUTINE_STEPS (name, sequence) VALUES 
('Oil Cleanser', 1), ('Water Cleanser', 2), ('Toner', 3), ('Serum', 4), ('SPF', 5);