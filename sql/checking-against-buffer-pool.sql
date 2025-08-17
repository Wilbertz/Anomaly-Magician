SELECT
    loc.file_id,
    loc.page_id,
    loc.slot_id,
    t.*
FROM dbo.samplecodestable t
CROSS APPLY sys.fn_PhysLocCracker(%%physloc%%) AS loc
WHERE EXISTS (
    SELECT 1
    FROM sys.dm_os_buffer_descriptors bd
    JOIN sys.allocation_units au
        ON bd.allocation_unit_id = au.allocation_unit_id
    JOIN sys.partitions p
        ON au.container_id = p.hobt_id
    WHERE bd.database_id = DB_ID()
      AND p.object_id = OBJECT_ID('dbo.samplecodestable')
      AND bd.file_id = loc.file_id
      AND bd.page_id = loc.page_id
);