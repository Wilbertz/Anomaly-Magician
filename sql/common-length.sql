SELECT LEN(value) AS Length, COUNT(*) AS Count FROM dbo.samplecodestable
GROUP BY LEN(VALUE)

SELECT 
    MIN(LEN(value)) AS MinLength,
    MAX(LEN(value)) AS MaxLength
FROM dbo.samplecodestable
WHERE value IS NOT NULL;