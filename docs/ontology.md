# Supply Chain Ontology Specification
**Database:** `ONTO_HACKATHON` | **Schema:** `CORE`

---

## 1. Core Entities (MVP 6)

### 1.1 SUPPLIER
- **Primary Key:** `supplier_id` (e.g. `S-001`, `S-017`)
- **Attributes:** `supplier_name`, `tier` (Tier 1/2/3), `country`, `risk_level` (Low/Medium/High/Critical)
- **Hierarchy:** `tier` -> `risk_level` -> `supplier_id`
- **Key Fixture:** `S-017` ("MicroCore Silicon Dynamics") is a Tier-1 Critical supplier associated with Scenario S1.

### 1.2 PART
- **Primary Key:** `part_id` (e.g. `PART-MCU-101`)
- **Attributes:** `part_name`, `category` (Electronics, Mechanical, Fasteners, Structural), `unit_cost`, `supplier_id` (FK)
- **Security:** `unit_cost` protected by `MASK_COST_DATA`. Visible only to `ONTO_PROCUREMENT` and `ONTO_JUDGE`.

### 1.3 PLANT
- **Primary Key:** `plant_id` (e.g. `P01`, `P03`, `P07`, `P09`)
- **Attributes:** `plant_name`, `region` (North America, EMEA, APAC), `country`
- **Hierarchy:** `region` -> `country` -> `plant_id`

### 1.4 CUSTOMER
- **Primary Key:** `customer_id` (e.g. `CUST-1001`)
- **Attributes:** `customer_name`, `segment` (Enterprise, Strategic, Commercial), `region`

### 1.5 ORDER_LINE
- **Primary Key:** `order_line_id`
- **Foreign Keys:** `order_id`, `part_id` (PART), `plant_id` (PLANT), `customer_id` (CUSTOMER)
- **Attributes:** `quantity_ordered`, `quantity_fulfilled`, `order_date`, `promised_date`
- **Trap Defense:** `is_delayed_legacy` is flagged as `DEPRECATED`. Computed from ship date; violates `OTD_V1`.

### 1.6 SHIPMENT
- **Primary Key:** `shipment_id` (e.g. `SH-93821`)
- **Foreign Key:** `order_line_id` (ORDER_LINE)
- **Attributes:** `carrier_id`, `lane_id` (e.g. `LANE-NW-04`), `ship_date`, `delivery_date`, `promised_date`, `delivery_status`, `freight_cost`
- **Security:** `freight_cost` protected by `MASK_COST_DATA`.

---

## 2. Relationships & Cardinalities

```
SUPPLIER   ──(1:N)──> PART
PART       ──(1:N)──> ORDER_LINE
PLANT      ──(1:N)──> ORDER_LINE
CUSTOMER   ──(1:N)──> ORDER_LINE
ORDER_LINE ──(1:N)──> SHIPMENT
```

- Explicit one-to-many joins.
- Eliminates Cartesian products and duplicate metric aggregations.
