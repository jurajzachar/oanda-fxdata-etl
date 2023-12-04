SELECT create_hypertable('oanda.fx_prices', 'time', chunk_time_interval => INTERVAL '24 hours');

-- create index on instrument code to make queries faster
CREATE INDEX IF NOT EXISTS fx_prices__instrument_index ON oanda.fx_prices USING HASH (instrument);

-- create a unique index on time and instrument columens to make sure we don't accidentally insert duplicate records

CREATE UNIQUE INDEX IF NOT EXISTS fx_prices__time_instrument_index ON oanda.fx_prices ("time", instrument);