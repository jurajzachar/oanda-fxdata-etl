-- creates timesclae's hyper table
select create_hypertable('oanda.fx_prices', 'time', 'instrument_code', 20)


create table if not exists "oanda.fx_files" (
  folder varchar(64) not null,
  filename varchar(64) not null,
  time_discovered    timestamp default current_timestamp,
  time_processed    timestamp default null,
  primary key (folder, filename)
);

CREATE TRIGGER IF NOT EXISTS ts_insert_blocker
    BEFORE INSERT
    ON oanda.fx_prices
    FOR EACH ROW
 EXECUTE FUNCTION _timescaledb_internal.insert_blocker();