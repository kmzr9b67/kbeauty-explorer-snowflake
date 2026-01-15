-- GENERATING THE RECOMMENDATION MATRIX

-- Clear the product table before re-generating data
TRUNCATE TABLE PRODUCTS;

-- Insert products using a CROSS JOIN to create a recommendation 
-- for every possible combination of user filters
INSERT INTO PRODUCTS (NAME, BRAND, RATING, SKIN_TYPE_ID, CONCERN_ID, AGE_RANGE_ID, STEP_ID)
SELECT 
    -- PRODUCT LOGIC: Assigning specific items based on Step, Skin Type, and Concern
    CASE rs.id
        WHEN 1 THEN -- Logic for Step 1: Oil Cleanser
            CASE 
                WHEN st.id = 2 THEN 'Heartleaf Pore Control Cleansing Oil' -- Oily Skin
                WHEN st.id = 4 THEN 'Calming Cleansing Oil'               -- Sensitive Skin
                WHEN c.id = 2 THEN 'Ginseng Cleansing Oil'                -- Aging Concern
                ELSE 'Gentle Black Fresh Cleansing Oil'
            END
        WHEN 2 THEN -- Logic for Step 2: Water Cleanser
            CASE 
                WHEN c.id = 1 THEN 'Salicylic Acid Daily Gentle Cleanser'  -- Acne
                WHEN st.id = 1 THEN 'Hyaluronic Acid Low pH Cleansing Foam'-- Dry Skin
                ELSE 'Low pH Good Morning Gel Cleanser'
            END
        WHEN 3 THEN -- Logic for Step 3: Toner
            CASE 
                WHEN c.id = 3 THEN 'Rice Toner'
                WHEN c.id = 1 THEN 'AHA/BHA Clarifying Toner'
                WHEN c.id = 5 THEN 'Supple Preparation Unscented Toner'
                ELSE 'Ginseng Essence Water'
            END
        WHEN 4 THEN -- Logic for Step 4: Serum
            CASE 
                WHEN c.id = 1 THEN 'Centella Ampoule'
                WHEN c.id = 2 THEN 'Retinol Cica Repair Ampoule'
                WHEN c.id = 4 THEN 'Glow Serum : Propolis + Niacinamide'
                ELSE 'Advanced Snail 96 Mucin Power Essence'
            END
        WHEN 5 THEN -- Logic for Step 5: Sunscreen
            CASE 
                WHEN st.id = 2 THEN 'Matte Sun Stick'
                WHEN st.id = 4 THEN 'Centella Green Level Unscented'
                ELSE 'Relief Sun : Rice + Probiotics'
            END
    END as name,
    
    -- BRAND LOGIC: Matching brands to the products selected above
    CASE rs.id
        WHEN 1 THEN CASE WHEN st.id = 2 THEN 'Anua' WHEN st.id = 4 THEN 'Pyunkang Yul' WHEN c.id = 2 THEN 'Beauty of Joseon' ELSE 'Dear Klairs' END
        WHEN 2 THEN CASE WHEN c.id = 1 THEN 'COSRX' WHEN st.id = 1 THEN 'Isntree' ELSE 'COSRX' END
        WHEN 3 THEN CASE WHEN c.id = 3 THEN 'I''m From' WHEN c.id = 1 THEN 'COSRX' WHEN c.id = 5 THEN 'Dear Klairs' ELSE 'Beauty of Joseon' END
        WHEN 4 THEN CASE WHEN c.id = 1 THEN 'SKIN1004' WHEN c.id = 2 THEN 'Innisfree' WHEN c.id = 4 THEN 'Beauty of Joseon' ELSE 'COSRX' END
        WHEN 5 THEN CASE WHEN st.id = 2 THEN 'Beauty of Joseon' WHEN st.id = 4 THEN 'Purito' ELSE 'Beauty of Joseon' END
    END as brand,

    -- RATING GENERATION: Generates a realistic rating between 4.5 and 5.0
    ROUND(UNIFORM(4.5::FLOAT, 5.0::FLOAT, RANDOM()), 1),
    
    st.id, c.id, ar.id, rs.id
FROM SKIN_TYPES st
CROSS JOIN CONCERNS c
CROSS JOIN AGE_RANGES ar
CROSS JOIN ROUTINE_STEPS rs;