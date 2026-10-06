-- =====================================================================
-- 03_CORE_DYNAMIC_TABLES.SQL — GOVERNED TRANSFORMATIONS
-- =====================================================================

USE DATABASE ONTO_HACKATHON;
USE SCHEMA CORE;

-- Dynamic Table: CORE_SUPPLIER
CREATE OR REPLACE DYNAMIC TABLE CORE_SUPPLIER
    TARGET_LAG = '1 MINUTE'
    WAREHOUSE = ONTO_WH
AS
SELECT 
    supplier_id,
    TRIM(supplier_name) AS supplier_name,
    tier,
    country,
    risk_level
FROM ONTO_HACKATHON.RAW.RAW_SUPPLIER;

-- Dynamic Table: CORE_PLANT
CREATE OR REPLACE DYNAMIC TABLE CORE_PLANT
    TARGET_LAG = '1 MINUTE'
    WAREHOUSE = ONTO_WH
AS
SELECT 
    plant_id,
    TRIM(plant_name) AS plant_name,
    region,
    country
FROM ONTO_HACKATHON.RAW.RAW_PLANT;

-- Dynamic Table: CORE_PART
CREATE OR REPLACE DYNAMIC TABLE CORE_PART
    TARGET_LAG = '1 MINUTE'
    WAREHOUSE = ONTO_WH
AS
SELECT 
    part_id,
    TRIM(part_name) AS part_name,
    category,
    unit_cost,
    supplier_id
FROM ONTO_HACKATHON.RAW.RAW_PART;

-- Dynamic Table: CORE_CUSTOMER
CREATE OR REPLACE DYNAMIC TABLE CORE_CUSTOMER
    TARGET_LAG = '1 MINUTE'
    WAREHOUSE = ONTO_WH
AS
SELECT 
    customer_id,
    TRIM(customer_name) AS customer_name,
    segment,
    region
FROM ONTO_HACKATHON.RAW.RAW_CUSTOMER;

-- Dynamic Table: CORE_ORDER_LINE
CREATE OR REPLACE DYNAMIC TABLE CORE_ORDER_LINE
    TARGET_LAG = '1 MINUTE'
    WAREHOUSE = ONTO_WH
AS
SELECT 
    order_line_id,
    order_id,
    part_id,
    plant_id,
    customer_id,
    quantity_ordered,
    quantity_fulfilled,
    order_date,
    promised_date,
    is_delayed_legacy
FROM ONTO_HACKATHON.RAW.RAW_ORDER_LINE;

-- Dynamic Table: CORE_SHIPMENT
CREATE OR REPLACE DYNAMIC TABLE CORE_SHIPMENT
    TARGET_LAG = '1 MINUTE'
    WAREHOUSE = ONTO_WH
AS
SELECT 
    shipment_id,
    order_line_id,
    carrier_id,
    lane_id,
    ship_date,
    delivery_date,
    promised_date,
    delivery_status,
    freight_cost
FROM ONTO_HACKATHON.RAW.RAW_SHIPMENT;

-- Dynamic Table: CORE_INVENTORY
CREATE OR REPLACE DYNAMIC TABLE CORE_INVENTORY
    TARGET_LAG = '1 MINUTE'
    WAREHOUSE = ONTO_WH
AS
SELECT 
    part_id,
    plant_id,
    current_stock_quantity,
    usage_quantity_30d,
    days_of_inventory,
    snapshot_date
FROM ONTO_HACKATHON.RAW.RAW_INVENTORY;
