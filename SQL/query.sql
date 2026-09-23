

-- QUERY 1: Isolate the High-Risk Cohort for the A/B Test Experiment
-- Evaluates employees working overtime, earning under 5000, and reporting low job satisfaction
SELECT 
    COUNT(*) AS Total_High_Risk_Staff,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Total_Left,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Baseline_Attrition_Rate_Pct
FROM employees
WHERE OverTime = 'Yes' 
  AND MonthlyIncome < 5000 
  AND JobSatisfaction <= 2;


-- QUERY 2: Breakdown Attrition Rates by Department
-- Groups metrics by active organizational segments
SELECT 
    Department,
    COUNT(*) AS Employee_Count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Dept_Attrition_Rate_Pct
FROM employees
GROUP BY Department
ORDER BY Dept_Attrition_Rate_Pct DESC;
