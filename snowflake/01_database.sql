-- =====================================================================
-- 01_DATABASE.SQL — ONTOLOGYONE INFRASTRUCTURE INITIALIZATION
-- Snowflake CoCo Hackathon Track 5
-- =====================================================================

USE ROLE ACCOUNTADMIN;

-- Dedicated Hackathon Warehouse
CREATE WAREHOUSE IF NOT EXISTS ONTO_WH
    WITH WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'OntologyOne supply chain analytics warehouse';

-- Dedicated Hackathon Database
CREATE DATABASE IF NOT EXISTS ONTO_HACKATHON
    COMMENT = 'OntologyOne Governed Supply Chain Database';

USE DATABASE ONTO_HACKATHON;

-- Architecture Schemas (5 Layers)
CREATE SCHEMA IF NOT EXISTS RAW
    COMMENT = 'Ingestion layer for raw enterprise feeds';

CREATE SCHEMA IF NOT EXISTS CORE
    COMMENT = 'Governed dynamic tables and semantic views';

CREATE SCHEMA IF NOT EXISTS MART
    COMMENT = 'Certified metrics marts (Two-tier truth architecture)';

CREATE SCHEMA IF NOT EXISTS GOV
    COMMENT = 'Security policies, masking functions, and audit logging';

CREATE SCHEMA IF NOT EXISTS DOCS
    COMMENT = 'Unstructured corpus and Cortex Search indexing';

-- Internal Stages for Semantic View and App artifacts
CREATE STAGE IF NOT EXISTS ONTO_HACKATHON.CORE.SEMANTIC_STAGE
    DIRECTORY = (ENABLE = TRUE)
    COMMENT = 'Stage storing semantic view YAML specifications';

CREATE STAGE IF NOT EXISTS ONTO_HACKATHON.CORE.STREAMLIT_STAGE
    DIRECTORY = (ENABLE = TRUE)
    COMMENT = 'Stage storing Streamlit in Snowflake code artifacts';

CREATE STAGE IF NOT EXISTS ONTO_HACKATHON.RAW.RAW_DATA_STAGE
    DIRECTORY = (ENABLE = TRUE)
    COMMENT = 'Stage storing CSV data fixtures';
