-- =====================================================================
-- GOLDEN QUERIES — VERIFIED BENCHMARKS FOR HACKATHON EVALUATION
-- =====================================================================

-- Golden Query 1: Flagship Q3 OTD (Target: 91.4%)
SELECT period, otd_rate, status 
FROM ONTO_HACKATHON.MART.MART_OTD_AGGREGATE 
WHERE period = '2026-Q3' AND supplier_id = 'ALL' AND plant_id = 'ALL';

-- Golden Query 2: S-017 Deterioration in Q3 (Target: 81.7%, 428 late shipments)
SELECT 
    p.supplier_id,
    COUNT(s.shipment_id) AS total_shipments,
    COUNT(CASE WHEN s.delivery_date <= s.promised_date THEN 1 END) AS on_time_shipments,
    COUNT(CASE WHEN s.delivery_date > s.promised_date THEN 1 END) AS late_shipments,
    ROUND((COUNT(CASE WHEN s.delivery_date <= s.promised_date THEN 1 END) / COUNT(s.shipment_id)) * 100, 1) AS otd_rate
FROM ONTO_HACKATHON.CORE.CORE_SHIPMENT s
JOIN ONTO_HACKATHON.CORE.CORE_ORDER_LINE o ON s.order_line_id = o.order_line_id
JOIN ONTO_HACKATHON.CORE.CORE_PART p ON o.part_id = p.part_id
WHERE p.supplier_id = 'S-017' AND s.delivery_date BETWEEN '2026-07-01' AND '2026-09-30'
GROUP BY p.supplier_id;

-- Golden Query 3: Plant P03 Fill Rate Bottleneck (Target: <78%)
SELECT 
    plant_id,
    ROUND((SUM(quantity_fulfilled) / SUM(quantity_ordered)) * 100, 1) AS fill_rate_pct
FROM ONTO_HACKATHON.CORE.CORE_ORDER_LINE
WHERE plant_id = 'P03'
GROUP BY plant_id;

-- Golden Query 4: Surcharge Spike on LANE-NW-04 (Target: +30% vs baseline)
SELECT 
    lane_id,
    ROUND(AVG(freight_cost), 2) AS avg_freight_cost
FROM ONTO_HACKATHON.CORE.CORE_SHIPMENT
GROUP BY lane_id;

-- Golden Query 5: Cross-Persona Aggregate OTD Consistency Check
-- Query returns 91.4% whether run by ONTO_PLANNER, ONTO_PROCUREMENT, ONTO_LOGISTICS, or ONTO_JUDGE
SELECT 
    '${CURRENT_ROLE}' AS persona_role,
    period,
    otd_rate
FROM ONTO_HACKATHON.MART.MART_OTD_AGGREGATE
WHERE period = '2026-Q3' AND supplier_id = 'ALL' AND plant_id = 'ALL';
