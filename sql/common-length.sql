SELECT LEN(value) AS Length, COUNT(*) AS Count FROM samplecodestable
GROUP BY LEN(VALUE)

DBCC SHOW_STATISTICS ("samplecodestable", "value");

SELECT 
    MIN(LEN(value)) AS MinLength,
    MAX(LEN(value)) AS MaxLength
FROM dbo.samplecodestable
WHERE value IS NOT NULL;