-- =====================================================================
-- RESET.SQL — DEMO & HACKATHON ENVIRONMENT RE-INITIALIZATION
-- Restores baseline state for deterministic demo replay
-- =====================================================================

USE ROLE ACCOUNTADMIN;
USE DATABASE ONTO_HACKATHON;

-- Clear Audit Log
TRUNCATE TABLE IF EXISTS ONTO_HACKATHON.GOV.AUDIT_LOG;

-- Re-seed Certified Aggregate Mart
INSERT OVERWRITE INTO ONTO_HACKATHON.MART.MART_OTD_AGGREGATE (period, supplier_id, plant_id, total_shipments, on_time_shipments, otd_rate, status)
VALUES
    ('2026-Q3', 'ALL', 'ALL', 10000, 9140, 91.4, 'CERTIFIED'),
    ('2026-Q2', 'ALL', 'ALL', 5000, 4740, 94.8, 'CERTIFIED'),
    ('2026-Q2', 'S-017', 'ALL', 1200, 1154, 96.2, 'CERTIFIED'),
    ('2026-Q3', 'S-017', 'ALL', 2339, 1911, 81.7, 'CERTIFIED'),
    ('2026-Q3', 'S-017', 'P03', 812, 655, 80.7, 'CERTIFIED'),
    ('2026-Q3', 'S-017', 'P07', 774, 638, 82.4, 'CERTIFIED'),
    ('2026-Q3', 'S-017', 'P09', 753, 618, 82.1, 'CERTIFIED');

-- Verify Dynamic Tables
ALTER DYNAMIC TABLE IF EXISTS ONTO_HACKATHON.CORE.CORE_ORDER_LINE REFRESH;
ALTER DYNAMIC TABLE IF EXISTS ONTO_HACKATHON.CORE.CORE_SHIPMENT REFRESH;

SELECT 'Demo environment reset complete. Unified truth ready for evaluation.' AS status;
