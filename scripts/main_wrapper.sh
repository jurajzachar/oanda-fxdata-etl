# env setup
export db_name=***
export db_user=***
export db_pwd=***
export db_host=localhost
export db_port=5432
export fx_folder=/path/to/gziped/files/

# sync files with orbital (market price collector)
rsync -avz "username@host:/path/to/gzipped/files/*.gz" $fx_folder

echo "------------------------------------------------------"
echo "I will now ingest collected market data to postgres..."
echo "------------------------------------------------------"

sleep 5

#python binary
oanda-fxdata-etl