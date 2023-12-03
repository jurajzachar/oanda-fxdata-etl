CREATE TABLE IF NOT EXISTS "oanda"."fx_prices"
(
    "time"            timestamp with time zone                          NOT NULL,
    instrument        character varying(8) COLLATE pg_catalog."default" NOT NULL,
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