-- =====================================================================
-- 06_CORTEX_SEARCH.SQL — UNSTRUCTURED EVIDENCE & CORTEX SEARCH
-- Snowflake CoCo Hackathon Track 5
-- =====================================================================

USE DATABASE ONTO_HACKATHON;
USE SCHEMA DOCS;

-- Table storing chunked unstructured legal and contractual documents
CREATE OR REPLACE TABLE CHUNKS (
    chunk_id    VARCHAR(64) PRIMARY KEY,
    doc_name    VARCHAR(128),
    title       VARCHAR(256),
    section     VARCHAR(128),
    content     TEXT,
    metadata    VARIANT,
    created_at  TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Seed chunks from corpus
INSERT OVERWRITE INTO CHUNKS (chunk_id, doc_name, title, section, content, metadata)
SELECT 
    'CHUNK_SLA_S017_01', 
    'SLA_S017.pdf', 
    'SLA S-017 Scope & Thresholds', 
    '§2 Performance Thresholds',
    'Supplier S-017 Committed On-Time Delivery (OTD): Supplier shall sustain a quarterly rolling On-Time Delivery Rate of >= 95.0%, computed against contractually agreed arrival dates (promised_date). Any calendar quarter wherein supplier OTD falls below 85.0% shall trigger executive vendor cure meetings.',
    PARSE_JSON('{"doc_type": "SLA", "supplier_id": "S-017", "section": "2"}')
UNION ALL
SELECT 
    'CHUNK_SLA_S017_02', 
    'SLA_S017.pdf', 
    'SLA S-017 Capacity Constraint & Lead-Time Revision', 
    '§4.2 Capacity Constraint & Lead-Time Revision',
    'Notice of Foundry Re-Tooling and Fab Allocation Restriction: Due to upstream wafer substrate shortage and scheduled clean-room maintenance at the Dresden Fab facility, Supplier S-017 has invoked Section 4.2 Allocation Procedures effective July 1, 2026 through September 30, 2026. Standard order lead time for the 17 active microcontroller part families is unilaterally revised from 14 calendar days to 28 calendar days. Fulfilling plants P03, P07, and P09 are placed on restricted daily allocation quotas.',
    PARSE_JSON('{"doc_type": "SLA", "supplier_id": "S-017", "section": "4.2", "clause": "Capacity Constraint"}')
UNION ALL
SELECT 
    'CHUNK_FREIGHT_01', 
    'freight_agreement.pdf', 
    'Freight Agreement Corridor LANE-NW-04 Surcharge', 
    '§2.1 Peak Maritime Congestion Surcharge',
    'Where regional port dwell times exceed 7.5 days or diesel fuel indices exceed National PADD 5 baseline by more than 15%, Carrier is entitled to invoke a Peak Maritime Congestion Surcharge. Effective July 15, 2026, an automatic +30% freight tariff surcharge is levied on all container shipments originating or terminating along transit lane LANE-NW-04.',
    PARSE_JSON('{"doc_type": "FREIGHT_AGREEMENT", "lane_id": "LANE-NW-04", "section": "2.1"}')
UNION ALL
SELECT 
    'CHUNK_MEMO_01', 
    'legacy_metric_memo.txt', 
    'Deprecation Memo: raw_orders.is_delayed', 
    'Governance Ruling',
    'The column raw_orders.is_delayed (and core_order_line.is_delayed_legacy) is declared DEPRECATED and strictly UNCERTIFIED. Legacy systems evaluated dock dispatch date rather than customer arrival date, reporting a deceptive ~94% OTD. All analytics must strictly query governed contract OTD_V1: delivered orders arriving at or before promised delivery date.',
    PARSE_JSON('{"doc_type": "GOVERNANCE_MEMO", "metric": "OTD_V1", "status": "DEPRECATED"}')
UNION ALL
SELECT 
    'CHUNK_POLICY_01', 
    'regional_policy.txt', 
    'Regional Capacity Balancing Policy', 
    '§3 Cross-Facility Reallocation Protocol',
    'When an individual plant\'s fill rate drops below 80.0% for two consecutive 14-day cycles: Operations leadership shall initiate a Dynamic Order Reallocation. Active unstarted purchase order lines scheduled for Plant P03 must be reassigned to Plant P07. Common sub-assembly buffer components shall be transferred via expedited ground shuttle from P03 to P07 within 48 hours.',
    PARSE_JSON('{"doc_type": "SOP", "plants": ["P03", "P07"], "section": "3"}');

-- Create Snowflake Cortex Search Service
CREATE OR REPLACE CORTEX SEARCH SERVICE ONTO_HACKATHON.DOCS.DOCS_SEARCH_SERVICE
    ON content
    ATTRIBUTES doc_name, title, section
    WAREHOUSE = ONTO_WH
    TARGET_LAG = '1 day'
AS (
    SELECT 
        chunk_id,
        doc_name,
        title,
        section,
        content
    FROM ONTO_HACKATHON.DOCS.CHUNKS
);

-- Grant Search Service to hackathon roles
GRANT USAGE ON CORTEX SEARCH SERVICE ONTO_HACKATHON.DOCS.DOCS_SEARCH_SERVICE TO ROLE ONTO_PLANNER;
GRANT USAGE ON CORTEX SEARCH SERVICE ONTO_HACKATHON.DOCS.DOCS_SEARCH_SERVICE TO ROLE ONTO_PROCUREMENT;
GRANT USAGE ON CORTEX SEARCH SERVICE ONTO_HACKATHON.DOCS.DOCS_SEARCH_SERVICE TO ROLE ONTO_LOGISTICS;
GRANT USAGE ON CORTEX SEARCH SERVICE ONTO_HACKATHON.DOCS.DOCS_SEARCH_SERVICE TO ROLE ONTO_JUDGE;
