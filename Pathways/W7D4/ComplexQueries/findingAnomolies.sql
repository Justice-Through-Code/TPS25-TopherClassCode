-- Finding Anomalies with Subqueries (Fixed Version)
-- Demonstrates using CTEs and subqueries for statistical analysis
-- This version resolves the nested aggregate function error

.headers on
.mode column
.width 15 15 10 10 10 10

.print "\n--- Finding temperature anomalies ---"

-- We use Common Table Expressions (CTEs) to break down the complex calculation
-- Think of CTEs as temporary result sets that we can reference multiple times
-- This approach solves the "nested aggregate function" problem

WITH city_averages AS (
    -- Step 1: Calculate the average temperature for each city
    -- This gives us our baseline "normal" temperature for each location
    SELECT 
        l.city,
        AVG(wr.temperature) AS avg_temp
    FROM weather_readings wr
    JOIN weather_stations ws ON wr.station_id = ws.station_id
    JOIN locations l ON ws.location_id = l.location_id
    GROUP BY l.city
),
city_stats AS (
    -- Step 2: Now calculate standard deviation using the averages we just computed
    -- Standard deviation measures how much temperatures typically vary from the average
    -- We can now reference ca.avg_temp because we calculated it in the previous step
    SELECT 
        ca.city,
        ca.avg_temp,
        SQRT(AVG((wr.temperature - ca.avg_temp) * (wr.temperature - ca.avg_temp))) AS std_dev
    FROM city_averages ca
    JOIN locations l ON ca.city = l.city
    JOIN weather_stations ws ON l.location_id = ws.location_id
    JOIN weather_readings wr ON ws.station_id = wr.station_id
    GROUP BY ca.city, ca.avg_temp
)
-- Step 3: Use our calculated statistics to identify temperature anomalies
SELECT 
    wr.reading_date,
    l.city,
    wr.temperature,
    cs.avg_temp,
    cs.std_dev,
    -- Z-score calculation: (actual - average) / standard_deviation
    -- This tells us how many standard deviations away from normal this reading is
    ROUND((wr.temperature - cs.avg_temp) / cs.std_dev, 2) AS z_score
FROM weather_readings wr
JOIN weather_stations ws ON wr.station_id = ws.station_id
JOIN locations l ON ws.location_id = l.location_id
JOIN city_stats cs ON l.city = cs.city
-- Filter for readings that are more than 1 standard deviation from normal
-- ABS() catches both extremely hot AND extremely cold anomalies
WHERE ABS((wr.temperature - cs.avg_temp) / cs.std_dev) > 1
-- Show the most extreme anomalies first
ORDER BY ABS((wr.temperature - cs.avg_temp) / cs.std_dev) DESC;

.print "\n--- Enhanced Explanation ---"
.print "This improved query fixes the nested aggregate function error by using CTEs:"
.print ""
.print "STEP 1 - Calculate Baselines:"
.print "  • First CTE (city_averages) computes average temperature for each city"
.print "  • This establishes what 'normal' means for each location"
.print ""
.print "STEP 2 - Calculate Variability:"
.print "  • Second CTE (city_stats) uses those averages to compute standard deviation"
.print "  • Standard deviation measures how much temperatures typically fluctuate"
.print "  • Now we can reference the previously calculated averages without nesting functions"
.print ""
.print "STEP 3 - Identify Anomalies:"
.print "  • Main query calculates z-scores using our pre-computed statistics"
.print "  • Z-score = (actual_temp - city_average) / city_std_deviation"
.print "  • Filters for readings with |z-score| > 1 (could use 2 or 3 for stricter criteria)"
.print "  • Results ordered by severity of anomaly"
.print ""
.print "WHY THIS APPROACH WORKS:"
.print "  • Breaks complex calculation into logical, sequential steps"
.print "  • Each CTE represents one conceptual operation"
.print "  • Avoids the SQL limitation of nested aggregate functions"
.print "  • Makes the statistical logic easier to understand and debug"
.print ""
.print "INTERPRETING RESULTS:"
.print "  • Z-score of +2.0 = temperature is 2 std deviations above city average (very hot)"
.print "  • Z-score of -1.5 = temperature is 1.5 std deviations below average (quite cold)"
.print "  • Z-scores near 0 = temperature close to typical for that city"