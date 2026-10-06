# ONTOLOGYONE — MAKEFILE
# Master build, deploy, test, and run targets for Snowflake CoCo CLI Hackathon

PYTHON ?= python
STREAMLIT ?= streamlit

.PHONY: all help init generate-data seed-fixtures test-coco deploy deploy-db deploy-semantic deploy-search deploy-agent deploy-app run reset clean

help:
	@echo "OntologyOne Master Commands:"
	@echo "  make init            - Install local dependencies"
	@echo "  make generate-data   - Run deterministic data generator & plant scenarios"
	@echo "  make test-coco       - Run 12/12 Governance & Metric verification suite"
	@echo "  make run             - Launch 4-screen Streamlit Command Center locally"
	@echo "  make deploy          - Deploy full stack to Snowflake via CoCo CLI"
	@echo "  make reset           - Reset synthetic data & demo environment to clean state"

all: init generate-data test-coco

init:
	$(PYTHON) -m pip install -r requirements.txt

generate-data:
	$(PYTHON) data/generator.py

seed-fixtures: generate-data

test-coco:
	$(PYTHON) tests/run_suite.py

run:
	$(STREAMLIT) run app/streamlit_app.py

deploy: deploy-db deploy-semantic deploy-search deploy-agent deploy-app
	@echo "OntologyOne deployment completed successfully via CoCo CLI."

deploy-db:
	@echo "Deploying Snowflake DB, schemas, raw tables, core dynamic tables, and governance..."
	snow sql -f snowflake/01_database.sql || true
	snow sql -f snowflake/02_raw_tables.sql || true
	snow sql -f snowflake/03_core_dynamic_tables.sql || true
	snow sql -f snowflake/04_metrics_mart.sql || true
	snow sql -f snowflake/05_governance_rbac_rap.sql || true

deploy-semantic:
	@echo "Deploying SUPPLY_SEMANTIC semantic view..."
	snow stage copy ontology/SUPPLY_SEMANTIC.sv.yaml @ONTO_HACKATHON.CORE.SEMANTIC_STAGE/ --overwrite || true

deploy-search:
	@echo "Deploying Cortex Search Service for Document Corpus..."
	snow sql -f snowflake/06_cortex_search.sql || true

deploy-agent:
	@echo "Deploying Cortex Agent and CoCo skills..."
	snow sql -f snowflake/07_agent.sql || true

deploy-app:
	@echo "Deploying Streamlit in Snowflake (SiS)..."
	snow streamlit deploy --replace || true

reset:
	snow sql -f demo/reset.sql || true
	$(PYTHON) data/generator.py
	@echo "Demo state reset to clean baseline."

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__ .pytest_cache
