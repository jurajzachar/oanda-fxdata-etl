CREATE TABLE IF NOT EXISTS "oanda"."fx_prices_historical"
(
    "time"            timestamp with time zone                          NOT NULL,
    instrument        character varying(24) COLLATE pg_catalog."default" NOT NULL,
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
    closeout_ask      double precision
)
PARTITION BY RANGE(time);

CREATE TABLE IF NOT EXISTS "oanda"."fx_prices_historical_2020" PARTITION OF "oanda"."fx_prices_historical" FOR VALUES FROM ('2020-01-01') TO ('2021-01-01');
CREATE TABLE IF NOT EXISTS "oanda"."fx_prices_historical_2021" PARTITION OF "oanda"."fx_prices_historical" FOR VALUES FROM ('2021-01-01') TO ('2022-01-01');
CREATE TABLE IF NOT EXISTS "oanda"."fx_prices_historical_2022" PARTITION OF "oanda"."fx_prices_historical" FOR VALUES FROM ('2022-01-01') TO ('2023-01-01');
CREATE TABLE IF NOT EXISTS "oanda"."fx_prices_historical_2023" PARTITION OF "oanda"."fx_prices_historical" FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');
CREATE TABLE IF NOT EXISTS "oanda"."fx_prices_historical_2024" PARTITION OF "oanda"."fx_prices_historical" FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
CREATE TABLE IF NOT EXISTS "oanda"."fx_prices_historical_2025" PARTITION OF "oanda"."fx_prices_historical" FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

-- create index on instrument code to make queries faster
CREATE INDEX IF NOT EXISTS fx_prices_historical__instrument_index ON oanda.fx_prices_historical USING HASH (instrument);

-- create a unique index on time and instrument columens to make sure we don't accidentally insert duplicate records

CREATE UNIQUE INDEX IF NOT EXISTS fx_prices_historical__time_instrument_index ON oanda.fx_prices_historical ("time", instrument);