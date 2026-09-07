-- 1. Gesamtes Einkaufsvolumen
SELECT
    ROUND(SUM(total_cost)::numeric, 2) AS einkaufsvolumen
FROM procurement;

-- 2. Reklamationsquote
SELECT
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE complaint = 'Ja')
        / COUNT(*),
        2
    ) AS reklamationsquote_prozent
FROM procurement;


-- 3. Einkaufsvolumen nach Lieferant
SELECT
    supplier,
    ROUND(SUM(total_cost)::numeric, 2) AS einkaufsvolumen
FROM procurement
GROUP BY supplier
ORDER BY einkaufsvolumen DESC;

-- 4. Lieferanten-Performance
SELECT
    supplier,
    ROUND(AVG(delivery_days)::numeric, 2) AS durchschnittliche_lieferzeit,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE complaint = 'Ja')
        / COUNT(*),
        2
    ) AS reklamationsquote_prozent,
    ROUND(SUM(total_cost)::numeric, 2) AS einkaufsvolumen
FROM procurement
GROUP BY supplier
ORDER BY reklamationsquote_prozent DESC;

-- 5. Monatliche Preisentwicklung
SELECT
    TO_CHAR(DATE_TRUNC('month', order_date), 'YYYY-MM') AS monat,
    ROUND(AVG(unit_price)::numeric, 2) AS durchschnittspreis
FROM procurement
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY DATE_TRUNC('month', order_date);

