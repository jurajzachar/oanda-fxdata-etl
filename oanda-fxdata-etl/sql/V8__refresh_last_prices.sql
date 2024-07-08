CREATE EXTENSION pg_cron;

-- refresh view every 12 hours
SELECT cron.schedule('0 */12 * * *', 'REFRESH MATERIALIZED VIEW oanda.latest_fx_prices');