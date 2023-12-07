insert into oanda.fx_prices_historical
select
 "time",
 instrument,
 bid_price_l1,
 bid_price_l2,
 bid_price_l3,
 ask_price_l1,
 ask_price_l2,
 ask_price_l3,
 bid_liquidity_l1,
 bid_liquidity_l2,
 bid_liquidity_l3,
 ask_liquidity_l1,
 ask_liquidity_l2,
 ask_liquidity_l3,
 closeout_bid,
 closeout_ask
from oanda.fx_prices where time > '2020-01-01' and time <= '2021-12-31' order by time asc
;