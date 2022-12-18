CREATE TABLE IF NOT EXISTS oanda.oanda_fx_files
(
    folder character varying(64) COLLATE pg_catalog."default" NOT NULL,
    filename character varying(64) COLLATE pg_catalog."default" NOT NULL,
    time_discovered timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    time_processed timestamp without time zone,
    CONSTRAINT oanda_fx_files_pkey PRIMARY KEY (folder, filename)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS oanda.oanda_fx_files
    OWNER to timescaledb;