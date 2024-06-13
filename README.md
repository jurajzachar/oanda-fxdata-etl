# oanda-fxdata-etl
ETL for Oanda FX tick data

## Build
```
poetry build
```

## Test
```
python -m unittest discover .
```

## Install
```
poetry run python ./installer.py
```

## Run
```
export db_name=somedb
export db_user=someuser
export db_pwd=somedbpwd
export db_host=localhost
export db_port=5432

$ ./dist/oanda-fxdata-etl
```
