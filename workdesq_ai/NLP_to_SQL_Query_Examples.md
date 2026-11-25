# WorkDesQ NLP-to-SQL Query Examples
## Comprehensive Guide for Natural Language Database Queries

---

## 1. EMPLOYEE PRODUCTIVITY QUERIES

### Query 1.1: Most Disciplined Employee
**Natural Language:** "Who is the most disciplined employee?"
**Alternative Phrasings:**
- "Show me the most productive employee"
- "Which employee works the most efficiently?"
- "Who has the best work habits?"

**SQL Query:**
```sql
SELECT 
    ud.username,
    ud.depid,
    d.name as department,
    COUNT(DISTINCT DATE(u11.startdatetime)) as days_worked,
    AVG(u11.duration) as avg_work_hours,
    SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) as total_productive_hours,
    SUM(CASE WHEN u11.status = 'Distracted' THEN u11.duration ELSE 0 END) as total_distracted_hours,
    ROUND(SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) / 
          NULLIF(SUM(u11.duration), 0) * 100, 2) as productivity_percentage
FROM userdetails ud
JOIN userdata11 u11 ON ud.userid = u11.userid
LEFT JOIN department d ON ud.depid = d.id
WHERE ud.connected = 1
GROUP BY ud.userid, ud.username, ud.depid, d.name
ORDER BY productivity_percentage DESC, total_productive_hours DESC
LIMIT 1;
```

**Expected Result:** Rajesh Kumar or Kavya Iyer (both have ~100% productivity)

---

### Query 1.2: Least Productive Employees
**Natural Language:** "Who are the least productive employees?"
**Alternative Phrasings:**
- "Show me employees with low productivity"
- "Which employees are underperforming?"
- "Who works the least?"

**SQL Query:**
```sql
SELECT 
    ud.username,
    d.name as department,
    ud.location,
    SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) as productive_hours,
    SUM(CASE WHEN u11.status = 'Distracted' THEN u11.duration ELSE 0 END) as distracted_hours,
    SUM(CASE WHEN u11.status = 'Idle' THEN u11.duration ELSE 0 END) as idle_hours,
    ROUND(SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) / 
          NULLIF(SUM(u11.duration), 0) * 100, 2) as productivity_percentage
FROM userdetails ud
JOIN userdata11 u11 ON ud.userid = u11.userid
LEFT JOIN department d ON ud.depid = d.id
WHERE ud.connected = 1
GROUP BY ud.userid, ud.username, d.name, ud.location
HAVING productivity_percentage < 60
ORDER BY productivity_percentage ASC
LIMIT 10;
```

**Expected Result:** Neha Gupta, Sneha Patel (high distraction rates)

---

## 2. YOUTUBE USAGE QUERIES

### Query 2.1: Employees Using YouTube
**Natural Language:** "Show me employees using YouTube"
**Alternative Phrasings:**
- "Who watches YouTube during work?"
- "List all employees accessing YouTube"
- "Find YouTube users"

**SQL Query:**
```sql
SELECT 
    ud.username,
    d.name as department,
    ud.location,
    COUNT(*) as youtube_sessions,
    SUM(u11.duration) as total_youtube_hours,
    GROUP_CONCAT(DISTINCT DATE(u11.startdatetime) ORDER BY u11.startdatetime) as dates_used
FROM userdetails ud
JOIN userdata11 u11 ON ud.userid = u11.userid
LEFT JOIN department d ON ud.depid = d.id
WHERE u11.appname LIKE '%YouTube%'
GROUP BY ud.userid, ud.username, d.name, ud.location
ORDER BY total_youtube_hours DESC;
```

**Expected Result:** Sneha Patel, Amit Singh, Neha Gupta, Aditya Joshi

---

### Query 2.2: YouTube Usage by Department
**Natural Language:** "Which department uses YouTube the most?"
**Alternative Phrasings:**
- "YouTube usage by department"
- "Show YouTube consumption per team"

**SQL Query:**
```sql
SELECT 
    d.name as department,
    COUNT(DISTINCT ud.userid) as employees_using_youtube,
    SUM(u11.duration) as total_youtube_hours,
    AVG(u11.duration) as avg_session_duration,
    ROUND(SUM(u11.duration) / COUNT(DISTINCT ud.userid), 2) as avg_hours_per_employee
FROM department d
JOIN userdetails ud ON d.id = ud.depid
JOIN userdata11 u11 ON ud.userid = u11.userid
WHERE u11.appname LIKE '%YouTube%'
GROUP BY d.id, d.name
ORDER BY total_youtube_hours DESC;
```

---

### Query 2.3: YouTube Usage Trend
**Natural Language:** "Show YouTube usage trend over time"
**SQL Query:**
```sql
SELECT 
    DATE(u11.startdatetime) as date,
    COUNT(DISTINCT u11.userid) as unique_users,
    COUNT(*) as total_sessions,
    SUM(u11.duration) as total_hours,
    AVG(u11.duration) as avg_session_duration
FROM userdata11 u11
WHERE u11.appname LIKE '%YouTube%'
GROUP BY DATE(u11.startdatetime)
ORDER BY date DESC;
```

---

## 3. SOCIAL MEDIA USAGE QUERIES

### Query 3.1: Social Media Users
**Natural Language:** "Who uses social media during work hours?"
**Alternative Phrasings:**
- "Show employees on Facebook/Instagram"
- "List social media usage"

**SQL Query:**
```sql
SELECT 
    ud.username,
    d.name as department,
    SUM(CASE WHEN u11.appname LIKE '%Facebook%' THEN u11.duration ELSE 0 END) as facebook_hours,
    SUM(CASE WHEN u11.appname LIKE '%Instagram%' THEN u11.duration ELSE 0 END) as instagram_hours,
    SUM(CASE WHEN u11.appname LIKE '%Twitter%' THEN u11.duration ELSE 0 END) as twitter_hours,
    SUM(CASE WHEN u11.appname LIKE '%LinkedIn%' THEN u11.duration ELSE 0 END) as linkedin_hours,
    SUM(CASE WHEN u11.appname LIKE '%Facebook%' OR u11.appname LIKE '%Instagram%' 
             OR u11.appname LIKE '%Twitter%' THEN u11.duration ELSE 0 END) as total_social_hours
FROM userdetails ud
JOIN userdata11 u11 ON ud.userid = u11.userid
LEFT JOIN department d ON ud.depid = d.id
WHERE u11.appname LIKE '%Facebook%' 
   OR u11.appname LIKE '%Instagram%' 
   OR u11.appname LIKE '%Twitter%'
   OR u11.appname LIKE '%LinkedIn%'
GROUP BY ud.userid, ud.username, d.name
HAVING total_social_hours > 0
ORDER BY total_social_hours DESC;
```

**Expected Result:** Sneha Patel, Aditya Joshi, Marketing team members

---

## 4. DEPARTMENT-WISE ANALYSIS

### Query 4.1: Department Productivity Ranking
**Natural Language:** "Rank departments by productivity"
**SQL Query:**
```sql
SELECT 
    d.name as department,
    COUNT(DISTINCT ud.userid) as total_employees,
    SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) as total_productive_hours,
    SUM(CASE WHEN u11.status = 'Distracted' THEN u11.duration ELSE 0 END) as total_distracted_hours,
    ROUND(AVG(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END), 2) as avg_productive_hours_per_employee,
    ROUND(SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) / 
          NULLIF(SUM(u11.duration), 0) * 100, 2) as department_productivity_percentage
FROM department d
JOIN userdetails ud ON d.id = ud.depid
JOIN userdata11 u11 ON ud.userid = u11.userid
GROUP BY d.id, d.name
ORDER BY department_productivity_percentage DESC;
```

**Expected Result:** Engineering, Finance, Customer Support at top

---

### Query 4.2: Engineering Team Performance
**Natural Language:** "Show me Engineering department performance"
**SQL Query:**
```sql
SELECT 
    ud.username,
    ud.location,
    COUNT(DISTINCT DATE(u11.startdatetime)) as days_active,
    SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) as productive_hours,
    ROUND(AVG(u11.duration), 2) as avg_session_duration,
    MAX(u11.enddatetime) as last_active
FROM userdetails ud
JOIN userdata11 u11 ON ud.userid = u11.userid
JOIN department d ON ud.depid = d.id
WHERE d.name = 'Engineering'
GROUP BY ud.userid, ud.username, ud.location
ORDER BY productive_hours DESC;
```

---

## 5. TIME-BASED QUERIES

### Query 5.1: Activity by Time of Day
**Natural Language:** "When are employees most active?"
**SQL Query:**
```sql
SELECT 
    HOUR(u11.startdatetime) as hour_of_day,
    COUNT(*) as total_sessions,
    COUNT(DISTINCT u11.userid) as active_employees,
    SUM(CASE WHEN u11.status = 'Working' THEN 1 ELSE 0 END) as productive_sessions,
    SUM(CASE WHEN u11.status = 'Distracted' THEN 1 ELSE 0 END) as distracted_sessions,
    ROUND(SUM(CASE WHEN u11.status = 'Working' THEN 1 ELSE 0 END) / 
          NULLIF(COUNT(*), 0) * 100, 2) as productivity_rate
FROM userdata11 u11
GROUP BY HOUR(u11.startdatetime)
ORDER BY hour_of_day;
```

---

### Query 5.2: Today's Activity
**Natural Language:** "Show me today's employee activity"
**SQL Query:**
```sql
SELECT 
    ud.username,
    d.name as department,
    u11.status,
    u11.appname,
    u11.duration as hours,
    u11.startdatetime,
    u11.enddatetime
FROM userdetails ud
JOIN userdata11 u11 ON ud.userid = u11.userid
LEFT JOIN department d ON ud.depid = d.id
WHERE DATE(u11.startdatetime) = CURDATE()
ORDER BY ud.username, u11.startdatetime;
```

---

### Query 5.3: Weekly Summary
**Natural Language:** "Give me a weekly activity summary"
**SQL Query:**
```sql
SELECT 
    ud.username,
    d.name as department,
    COUNT(DISTINCT DATE(u11.startdatetime)) as days_worked,
    SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) as total_work_hours,
    SUM(CASE WHEN u11.status = 'Distracted' THEN u11.duration ELSE 0 END) as total_distraction_hours,
    ROUND(AVG(u11.duration), 2) as avg_daily_hours
FROM userdetails ud
JOIN userdata11 u11 ON ud.userid = u11.userid
LEFT JOIN department d ON ud.depid = d.id
WHERE u11.startdatetime >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
GROUP BY ud.userid, ud.username, d.name
ORDER BY total_work_hours DESC;
```

---

## 6. APPLICATION USAGE ANALYSIS

### Query 6.1: Most Used Applications
**Natural Language:** "What are the most used applications?"
**SQL Query:**
```sql
SELECT 
    TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(u11.appname, ',', numbers.n), ',', -1)) as application,
    COUNT(*) as usage_count,
    COUNT(DISTINCT u11.userid) as unique_users,
    SUM(u11.duration) as total_hours
FROM userdata11 u11
CROSS JOIN (
    SELECT 1 n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
    UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
) numbers
WHERE CHAR_LENGTH(u11.appname) - CHAR_LENGTH(REPLACE(u11.appname, ',', '')) >= numbers.n - 1
GROUP BY application
ORDER BY usage_count DESC
LIMIT 20;
```

---

### Query 6.2: Development Tool Usage
**Natural Language:** "Which development tools are most popular?"
**SQL Query:**
```sql
SELECT 
    ud.username,
    d.name as department,
    SUM(CASE WHEN u11.appname LIKE '%VS Code%' OR u11.appname LIKE '%Visual Studio Code%' 
             THEN u11.duration ELSE 0 END) as vscode_hours,
    SUM(CASE WHEN u11.appname LIKE '%IntelliJ%' THEN u11.duration ELSE 0 END) as intellij_hours,
    SUM(CASE WHEN u11.appname LIKE '%PyCharm%' THEN u11.duration ELSE 0 END) as pycharm_hours,
    SUM(CASE WHEN u11.appname LIKE '%Xcode%' THEN u11.duration ELSE 0 END) as xcode_hours
FROM userdetails ud
JOIN userdata11 u11 ON ud.userid = u11.userid
LEFT JOIN department d ON ud.depid = d.id
WHERE d.name = 'Engineering'
GROUP BY ud.userid, ud.username, d.name
ORDER BY (vscode_hours + intellij_hours + pycharm_hours + xcode_hours) DESC;
```

---

## 7. EMPLOYEE STATUS QUERIES

### Query 7.1: Currently Active Employees
**Natural Language:** "Who is currently online?"
**SQL Query:**
```sql
SELECT 
    ud.username,
    d.name as department,
    ud.location,
    ud.active as last_seen,
    ud.connected,
    TIMESTAMPDIFF(MINUTE, ud.active, NOW()) as minutes_since_activity
FROM userdetails ud
LEFT JOIN department d ON ud.depid = d.id
WHERE ud.connected = 1 
  AND TIMESTAMPDIFF(HOUR, ud.active, NOW()) < 1
ORDER BY ud.active DESC;
```

---

### Query 7.2: Offline Employees
**Natural Language:** "Which employees are offline?"
**SQL Query:**
```sql
SELECT 
    ud.username,
    d.name as department,
    ud.location,
    ud.active as last_seen,
    ud.connected,
    TIMESTAMPDIFF(HOUR, ud.active, NOW()) as hours_offline
FROM userdetails ud
LEFT JOIN department d ON ud.depid = d.id
WHERE ud.connected = 0 
   OR TIMESTAMPDIFF(HOUR, ud.active, NOW()) > 2
ORDER BY hours_offline DESC;
```

---

## 8. LOCATION-BASED QUERIES

### Query 8.1: Productivity by Location
**Natural Language:** "Compare productivity across locations"
**SQL Query:**
```sql
SELECT 
    ud.location,
    COUNT(DISTINCT ud.userid) as total_employees,
    SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) as total_productive_hours,
    ROUND(AVG(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END), 2) as avg_productive_hours,
    ROUND(SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) / 
          NULLIF(SUM(u11.duration), 0) * 100, 2) as productivity_percentage
FROM userdetails ud
JOIN userdata11 u11 ON ud.userid = u11.userid
GROUP BY ud.location
ORDER BY productivity_percentage DESC;
```

---

### Query 8.2: Bangalore Office Performance
**Natural Language:** "How is the Bangalore office performing?"
**SQL Query:**
```sql
SELECT 
    ud.username,
    d.name as department,
    SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) as productive_hours,
    COUNT(DISTINCT DATE(u11.startdatetime)) as days_active,
    ROUND(SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) / 
          NULLIF(SUM(u11.duration), 0) * 100, 2) as productivity_percentage
FROM userdetails ud
JOIN userdata11 u11 ON ud.userid = u11.userid
LEFT JOIN department d ON ud.depid = d.id
WHERE ud.location = 'Bangalore'
GROUP BY ud.userid, ud.username, d.name
ORDER BY productivity_percentage DESC;
```

---

## 9. WORK PATTERN ANALYSIS

### Query 9.1: Early Birds vs Night Owls
**Natural Language:** "Who starts work earliest?"
**SQL Query:**
```sql
SELECT 
    ud.username,
    d.name as department,
    MIN(TIME(u11.startdatetime)) as earliest_start,
    MAX(TIME(u11.enddatetime)) as latest_end,
    AVG(TIMESTAMPDIFF(HOUR, u11.startdatetime, u11.enddatetime)) as avg_work_duration
FROM userdetails ud
JOIN userdata11 u11 ON ud.userid = u11.userid
LEFT JOIN department d ON ud.depid = d.id
WHERE u11.status = 'Working'
GROUP BY ud.userid, ud.username, d.name
ORDER BY earliest_start ASC;
```

---

### Query 9.2: Break Pattern Analysis
**Natural Language:** "Show employee break patterns"
**SQL Query:**
```sql
SELECT 
    ud.username,
    d.name as department,
    COUNT(CASE WHEN u11.status = 'Break' THEN 1 END) as break_count,
    SUM(CASE WHEN u11.status = 'Break' THEN u11.duration ELSE 0 END) as total_break_hours,
    ROUND(AVG(CASE WHEN u11.status = 'Break' THEN u11.duration ELSE 0 END), 2) as avg_break_duration
FROM userdetails ud
JOIN userdata11 u11 ON ud.userid = u11.userid
LEFT JOIN department d ON ud.depid = d.id
GROUP BY ud.userid, ud.username, d.name
HAVING break_count > 0
ORDER BY total_break_hours DESC;
```

---

## 10. ADVANCED ANALYTICS

### Query 10.1: Productivity Correlation with Work Hours
**Natural Language:** "Is there a correlation between work hours and productivity?"
**SQL Query:**
```sql
SELECT 
    CASE 
        WHEN total_hours < 6 THEN '< 6 hours'
        WHEN total_hours BETWEEN 6 AND 7 THEN '6-7 hours'
        WHEN total_hours BETWEEN 7 AND 8 THEN '7-8 hours'
        WHEN total_hours > 8 THEN '> 8 hours'
    END as work_hour_range,
    COUNT(DISTINCT ud.userid) as employee_count,
    ROUND(AVG(productivity_pct), 2) as avg_productivity
FROM (
    SELECT 
        ud.userid,
        SUM(u11.duration) as total_hours,
        SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) / 
        NULLIF(SUM(u11.duration), 0) * 100 as productivity_pct
    FROM userdetails ud
    JOIN userdata11 u11 ON ud.userid = u11.userid
    GROUP BY ud.userid
) as subquery
JOIN userdetails ud ON subquery.userid = ud.userid
GROUP BY work_hour_range
ORDER BY work_hour_range;
```

---

### Query 10.2: Top Performers This Month
**Natural Language:** "Show top performers this month"
**SQL Query:**
```sql
SELECT 
    ud.username,
    d.name as department,
    ud.location,
    COUNT(DISTINCT DATE(u11.startdatetime)) as days_worked,
    SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) as productive_hours,
    ROUND(SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) / 
          NULLIF(SUM(u11.duration), 0) * 100, 2) as productivity_percentage,
    RANK() OVER (ORDER BY SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) DESC) as rank_by_hours,
    RANK() OVER (ORDER BY SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) / 
                 NULLIF(SUM(u11.duration), 0) DESC) as rank_by_productivity
FROM userdetails ud
JOIN userdata11 u11 ON ud.userid = u11.userid
LEFT JOIN department d ON ud.depid = d.id
WHERE u11.startdatetime >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY ud.userid, ud.username, d.name, ud.location
ORDER BY productivity_percentage DESC, productive_hours DESC
LIMIT 10;
```

---

## 11. SCREENSHOT ANALYSIS

### Query 11.1: Screenshot Capture Frequency
**Natural Language:** "How many screenshots were captured today?"
**SQL Query:**
```sql
SELECT 
    ud.username,
    d.name as department,
    COUNT(*) as screenshot_count,
    MIN(u12.time) as first_screenshot,
    MAX(u12.time) as last_screenshot
FROM userdetails ud
JOIN userdata12 u12 ON ud.userid = u12.userid
LEFT JOIN department d ON ud.depid = d.id
WHERE DATE(u12.time) = CURDATE()
GROUP BY ud.userid, ud.username, d.name
ORDER BY screenshot_count DESC;
```

---

### Query 11.2: Screenshot Timeline
**Natural Language:** "Show screenshot timeline for a specific user"
**SQL Query:**
```sql
SELECT 
    u12.path as screenshot_file,
    u12.time as captured_at,
    TIMESTAMPDIFF(MINUTE, 
        LAG(u12.time) OVER (ORDER BY u12.time), 
        u12.time) as minutes_since_last
FROM userdata12 u12
WHERE u12.userid = 1 
  AND DATE(u12.time) = CURDATE()
ORDER BY u12.time;
```

---

## 12. COMPLIANCE & MONITORING

### Query 12.1: Employees Violating Work Hours Policy
**Natural Language:** "Who is not following work hour policies?"
**SQL Query:**
```sql
SELECT 
    ud.username,
    d.name as department,
    ud.starttime as policy_start,
    ud.endtime as policy_end,
    MIN(TIME(u11.startdatetime)) as actual_start,
    MAX(TIME(u11.enddatetime)) as actual_end,
    CASE 
        WHEN MIN(TIME(u11.startdatetime)) > ud.starttime THEN 'Late Start'
        WHEN MAX(TIME(u11.enddatetime)) < ud.endtime THEN 'Early Leave'
        ELSE 'Compliant'
    END as violation_type
FROM userdetails ud
JOIN userdata11 u11 ON ud.userid = u11.userid
LEFT JOIN department d ON ud.depid = d.id
WHERE DATE(u11.startdatetime) = CURDATE()
GROUP BY ud.userid, ud.username, d.name, ud.starttime, ud.endtime
HAVING violation_type != 'Compliant'
ORDER BY violation_type;
```

---

## 13. COMPARATIVE ANALYSIS

### Query 13.1: Department Comparison
**Natural Language:** "Compare Engineering vs Sales productivity"
**SQL Query:**
```sql
SELECT 
    d.name as department,
    COUNT(DISTINCT ud.userid) as team_size,
    SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) as total_productive_hours,
    ROUND(AVG(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END), 2) as avg_hours_per_employee,
    ROUND(SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) / 
          NULLIF(SUM(u11.duration), 0) * 100, 2) as productivity_rate
FROM department d
JOIN userdetails ud ON d.id = ud.depid
JOIN userdata11 u11 ON ud.userid = u11.userid
WHERE d.name IN ('Engineering', 'Sales')
GROUP BY d.name
ORDER BY productivity_rate DESC;
```

---

## 14. TREND ANALYSIS

### Query 14.1: Productivity Trend
**Natural Language:** "Show productivity trend for last 30 days"
**SQL Query:**
```sql
SELECT 
    DATE(u11.startdatetime) as date,
    COUNT(DISTINCT u11.userid) as active_employees,
    SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) as total_productive_hours,
    ROUND(SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) / 
          NULLIF(SUM(u11.duration), 0) * 100, 2) as productivity_percentage
FROM userdata11 u11
WHERE u11.startdatetime >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY DATE(u11.startdatetime)
ORDER BY date DESC;
```

---

## COMPLEX MULTI-JOIN QUERIES

### Complex Query 1: Comprehensive Employee Report
**Natural Language:** "Generate a comprehensive report for all employees"
**SQL Query:**
```sql
SELECT 
    ud.username,
    d.name as department,
    ud.location,
    ud.os,
    ud.devicename,
    COUNT(DISTINCT DATE(u11.startdatetime)) as days_active,
    SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) as productive_hours,
    SUM(CASE WHEN u11.status = 'Distracted' THEN u11.duration ELSE 0 END) as distracted_hours,
    SUM(CASE WHEN u11.appname LIKE '%YouTube%' THEN u11.duration ELSE 0 END) as youtube_hours,
    COUNT(DISTINCT u12.id) as screenshot_count,
    ROUND(SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) / 
          NULLIF(SUM(u11.duration), 0) * 100, 2) as productivity_percentage,
    ud.active as last_seen,
    CASE 
        WHEN ud.connected = 1 THEN 'Online'
        WHEN ud.connected = 0 THEN 'Offline'
        ELSE 'Uninstalled'
    END as status
FROM userdetails ud
LEFT JOIN department d ON ud.depid = d.id
LEFT JOIN userdata11 u11 ON ud.userid = u11.userid
LEFT JOIN userdata12 u12 ON ud.userid = u12.userid
GROUP BY ud.userid, ud.username, d.name, ud.location, ud.os, ud.devicename, ud.active, ud.connected
ORDER BY productivity_percentage DESC;
```

---

## DASHBOARD METRICS

### Dashboard Query: Real-time Overview
**Natural Language:** "Show me the company dashboard"
**SQL Query:**
```sql
SELECT 
    'Total Employees' as metric,
    COUNT(DISTINCT ud.userid) as value
FROM userdetails ud
WHERE ud.connected IN (0, 1)

UNION ALL

SELECT 
    'Currently Active',
    COUNT(DISTINCT ud.userid)
FROM userdetails ud
WHERE ud.connected = 1 
  AND TIMESTAMPDIFF(MINUTE, ud.active, NOW()) < 30

UNION ALL

SELECT 
    'Average Productivity %',
    ROUND(AVG(productivity_pct), 2)
FROM (
    SELECT 
        SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END) / 
        NULLIF(SUM(u11.duration), 0) * 100 as productivity_pct
    FROM userdata11 u11
    WHERE DATE(u11.startdatetime) = CURDATE()
    GROUP BY u11.userid
) as subquery

UNION ALL

SELECT 
    'Total Work Hours Today',
    ROUND(SUM(CASE WHEN u11.status = 'Working' THEN u11.duration ELSE 0 END), 2)
FROM userdata11 u11
WHERE DATE(u11.startdatetime) = CURDATE();
```

---

## Notes for NLP Model Training:
1. Train on variations of questions (shown in alternative phrasings)
2. Handle synonyms: "productive" = "efficient" = "disciplined"
3. Time references: "today", "this week", "last month"
4. Comparative queries: "better than", "worse than", "compared to"
5. Aggregation keywords: "total", "average", "sum", "count"
6. Ranking keywords: "top", "best", "worst", "most", "least"
7. Filter keywords: "using", "accessing", "with", "having"

