DROP TYPE IF EXISTS "trading_venue";
CREATE TYPE "trading_venue" AS ENUM
    ('oanda');

ALTER TYPE "trading_venue"
    OWNER TO maintainer;

CREATE TABLE IF NOT EXISTS "fx_prices"
(
    source            "trading_venue" DEFAULT 'oanda'::"trading_venue",
    "time"            timestamp with time zone                           NOT NULL,
    currency_code     character varying(10) COLLATE pg_catalog."default" NOT NULL,
    bid_price_l1      double precision,
    bid_price_l2      double precision,
    bid_price_l3      double precision,
    ask_price_l1      double precision,
    ask_price_l2      double precision,
    ask_price_l3      double precision,
    bid_liquidity_l1  integer,
    bid_liquidity_l2  integer,
    bid_liquidity_l3  integer,
    ask_liquidity_l1  integer,
    ask_liquidity_l2  integer,
    ask_liquidity_l3  integer,
    closeout_bid      double precision,
    closeout_ask      double precision,
    closeout_midpoint double precision GENERATED ALWAYS AS (((closeout_ask - (closeout_bid / (2)::double precision)) + closeout_bid)) STORED
) TABLESPACE pg_default;

ALTER TABLE IF EXISTS "fx_prices"
    OWNER to maintainer;

CREATE INDEX IF NOT EXISTS "oanda_fx_prices_time_idx"
    ON "fx_prices" USING btree
        ("time" DESC NULLS FIRST)
    TABLESPACE pg_default;