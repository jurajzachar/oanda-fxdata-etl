---
WITH duplicates AS (
    SELECT
        path,
        MIN(time_discovered) AS earliest_time
    FROM oanda.fx_files
    GROUP BY path
),
to_delete AS (
    SELECT f.*
    FROM oanda.fx_files f
    LEFT JOIN duplicates d
    ON f.path = d.path AND f.time_discovered = d.earliest_time
    WHERE d.earliest_time IS NULL
)
DELETE FROM oanda.fx_files
WHERE ctid IN (SELECT ctid FROM to_delete);