CREATE MATERIALIZED VIEW oanda.latest_fx_prices AS
SELECT
    p.instrument,
    p.bid_price_l1 AS bid,
    p.ask_price_l1 AS ask,
    p.time
FROM
    oanda.fx_prices p
JOIN (
    SELECT
        instrument,
        MAX(time) AS max_time
    FROM
        oanda.fx_prices
    GROUP BY
        instrument
) AS latest
ON
    p.instrument = latest.instrument
    AND p.time = latest.max_time;

-- Query from the materialized view instead of the original table
SELECT
    instrument,
    bid,
    ask,
    time
FROM
    oanda.latest_fx_prices;