-- =====================================================================
-- 07_AGENT.SQL — CORTEX AGENT ORCHESTRATION & TOOL ROUTING
-- Snowflake CoCo Hackathon Track 5
-- =====================================================================

USE DATABASE ONTO_HACKATHON;
USE SCHEMA CORE;

-- Register Stage for Agent specifications
CREATE OR REPLACE STAGE AGENT_STAGE
    DIRECTORY = (ENABLE = TRUE);

-- Create Cortex Agent definition referencing Semantic View and Cortex Search
-- Modern architecture: One Cortex Agent orchestrating Cortex Analyst + Cortex Search
/*
CREATE OR REPLACE CORTEX AGENT ONTO_HACKATHON.CORE.ONTOLOGY_AGENT
    COMMENT = 'OntologyOne Governed Conversational Agent'
    SPEC = '{
        "model": "snowflake-arctic",
        "instructions": "You are OntologyOne, the governed supply chain intelligence agent for the enterprise. You operate under strict metric contracts (OTD_V1, FR_V1, DOI_V1, LC_V1). You ALWAYS cite governed metric definitions, provide generated governed SQL with grounding badges, and refuse deprecated trap columns (such as raw_orders.is_delayed). You always label recommendations as AI-generated recommendations.",
        "tools": [
            {
                "tool_spec": {
                    "type": "cortex_analyst_text_to_sql",
                    "name": "supply_chain_semantic_analyst",
                    "semantic_view": "ONTO_HACKATHON.CORE.SUPPLY_SEMANTIC"
                }
            },
            {
                "tool_spec": {
                    "type": "cortex_search",
                    "name": "supply_chain_docs_search",
                    "service": "ONTO_HACKATHON.DOCS.DOCS_SEARCH_SERVICE"
                }
            }
        ]
    }';
*/

-- Grant execution permissions
GRANT USAGE ON DATABASE ONTO_HACKATHON TO ROLE ONTO_PLANNER;
GRANT USAGE ON SCHEMA ONTO_HACKATHON.CORE TO ROLE ONTO_PLANNER;
GRANT USAGE ON STAGE ONTO_HACKATHON.CORE.AGENT_STAGE TO ROLE ONTO_PLANNER;
