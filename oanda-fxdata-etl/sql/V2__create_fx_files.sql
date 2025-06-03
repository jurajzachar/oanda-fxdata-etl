CREATE TABLE IF NOT EXISTS "oanda"."fx_files"
(
    path            character varying(200) PRIMARY KEY,
    time_discovered timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    time_processed  timestamp without time zone
)
    TABLESPACE pg_default;

