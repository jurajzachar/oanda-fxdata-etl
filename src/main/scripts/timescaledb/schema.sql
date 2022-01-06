-- schema for trading venues
drop type if exists "trading_venue" cascade ;
create type "trading_venue" as enum('oanda');

-- schema for oanda fx price ticks
drop table if exists "oanda_fx_prices";
create table "oanda_fx_prices" (
    source  trading_venue default 'oanda',
    time    timestamp with time zone not null,
    instrument_code   varchar(10) not null,
    bid_price_l1    double precision,
    bid_price_l2    double precision,
    bid_price_l3    double precision,
    ask_price_l1    double precision,
    ask_price_l2    double precision,
    ask_price_l3    double precision,
    bid_liquidity_l1    integer,
    bid_liquidity_l2    integer,
    bid_liquidity_l3    integer,
    ask_liquidity_l1    integer,
    ask_liquidity_l2    integer,
    ask_liquidity_l3    integer,
    closeout_bid    double precision,
    closeout_ask    double precision,
    closeout_midpoint double precision generated always as ((closeout_ask - closeout_bid / 2) + closeout_bid) stored
);

select create_hypertable('oanda_fx_prices', 'time', 'instrument_code', 20)