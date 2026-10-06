-- =====================================================================
-- 02_RAW_TABLES.SQL — INGESTION LAYER TABLES
-- =====================================================================

USE DATABASE ONTO_HACKATHON;
USE SCHEMA RAW;

-- 1. RAW SUPPLIERS
CREATE OR REPLACE TABLE RAW_SUPPLIER (
    supplier_id   VARCHAR(32) PRIMARY KEY,
    supplier_name VARCHAR(256),
    tier          VARCHAR(32),
    country       VARCHAR(64),
    risk_level    VARCHAR(32),
    ingested_at   TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 2. RAW PLANTS
CREATE OR REPLACE TABLE RAW_PLANT (
    plant_id    VARCHAR(32) PRIMARY KEY,
    plant_name  VARCHAR(256),
    region      VARCHAR(64),
    country     VARCHAR(64),
    ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 3. RAW PARTS
CREATE OR REPLACE TABLE RAW_PART (
    part_id     VARCHAR(64) PRIMARY KEY,
    part_name   VARCHAR(256),
    category    VARCHAR(64),
    unit_cost   FLOAT,
    supplier_id VARCHAR(32),
    ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 4. RAW CUSTOMERS
CREATE OR REPLACE TABLE RAW_CUSTOMER (
    customer_id   VARCHAR(64) PRIMARY KEY,
    customer_name VARCHAR(256),
    segment       VARCHAR(64),
    region        VARCHAR(64),
    ingested_at   TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 5. RAW ORDER LINES (includes legacy is_delayed trap)
CREATE OR REPLACE TABLE RAW_ORDER_LINE (
    order_line_id       VARCHAR(64) PRIMARY KEY,
    order_id            VARCHAR(64),
    part_id             VARCHAR(64),
    plant_id            VARCHAR(32),
    customer_id         VARCHAR(64),
    quantity_ordered    INT,
    quantity_fulfilled  INT,
    order_date          DATE,
    promised_date       DATE,
    is_delayed_legacy   BOOLEAN,
    ingested_at         TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 6. RAW SHIPMENTS
CREATE OR REPLACE TABLE RAW_SHIPMENT (
    shipment_id     VARCHAR(64) PRIMARY KEY,
    order_line_id   VARCHAR(64),
    carrier_id      VARCHAR(32),
    lane_id         VARCHAR(64),
    ship_date       DATE,
    delivery_date   DATE,
    promised_date   DATE,
    delivery_status VARCHAR(64),
    freight_cost    FLOAT,
    ingested_at     TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 7. RAW INVENTORY
CREATE OR REPLACE TABLE RAW_INVENTORY (
    part_id                 VARCHAR(64),
    plant_id                VARCHAR(32),
    current_stock_quantity  INT,
    usage_quantity_30d      INT,
    days_of_inventory       FLOAT,
    snapshot_date           DATE,
    ingested_at             TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
