CREATE TABLE IF NOT EXISTS "fx_files"
(
    path            character varying(128) COLLATE pg_catalog."default" NOT NULL,
    time_discovered timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    time_processed  timestamp without time zone,
    CONSTRAINT oanda_fx_files_pkey PRIMARY KEY (path)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS "fx_files"
    OWNER to maintainer;