IF EXISTS (
    SELECT 1
    FROM samplecodestable
    WHERE LEN(value) <> 5
)
    PRINT 'Some rows do not match';
ELSE
    PRINT 'All rows match';