-- Table: public.oanda_fx_prices

-- DROP TABLE IF EXISTS public.oanda_fx_prices;

-- Type: trading_venue

-- DROP TYPE IF EXISTS public.trading_venue;

CREATE TYPE IF NOT EXISTS oanda.trading_venue AS ENUM
    ('oanda');

ALTER TYPE oanda.trading_venue
    OWNER TO timescaledb;

CREATE TABLE IF NOT EXISTS oanda.fx_prices
(
    source oanda.trading_venue DEFAULT 'oanda'::oanda.trading_venue,
    "time" timestamp with time zone NOT NULL,
    currency_code character varying(10) COLLATE pg_catalog."default" NOT NULL,
    bid_price_l1 double precision,
    bid_price_l2 double precision,
    bid_price_l3 double precision,
    ask_price_l1 double precision,
    ask_price_l2 double precision,
    ask_price_l3 double precision,
    bid_liquidity_l1 integer,
    bid_liquidity_l2 integer,
    bid_liquidity_l3 integer,
    ask_liquidity_l1 integer,
    ask_liquidity_l2 integer,
    ask_liquidity_l3 integer,
    closeout_bid double precision,
    closeout_ask double precision,
    closeout_midpoint double precision GENERATED ALWAYS AS (((closeout_ask - (closeout_bid / (2)::double precision)) + closeout_bid)) STORED
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS oanda.fx_prices
    OWNER to timescaledb;
-- Index: oanda_fx_prices_currency_code_time_idx

-- DROP INDEX IF EXISTS public.oanda_fx_prices_currency_code_time_idx;

CREATE INDEX IF NOT EXISTS oanda_fx_prices_currency_code_time_idx
    ON oanda.fx_prices USING btree
    (currency_code COLLATE pg_catalog."default" ASC NULLS LAST, "time" DESC NULLS FIRST)
    TABLESPACE pg_default;
-- Index: oanda_fx_prices_time_idx

-- DROP INDEX IF EXISTS public.oanda_fx_prices_time_idx;

CREATE INDEX IF NOT EXISTS oanda_fx_prices_time_idx
    ON oanda.fx_prices USING btree
    ("time" DESC NULLS FIRST)
    TABLESPACE pg_default;

-- Trigger: ts_insert_blocker

-- DROP TRIGGER IF EXISTS ts_insert_blocker ON public.oanda_fx_prices;

CREATE TRIGGER ts_insert_blocker
    BEFORE INSERT
    ON oanda.fx_prices
    FOR EACH ROW
    EXECUTE FUNCTION _timescaledb_internal.insert_blocker();