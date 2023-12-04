import logging
import os.path
from random import randrange
from threading import Thread

from config import *
from db import Persistence
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fs import list_in_dir, read_oanda_streams_file

app = FastAPI()
app.mount("/static", StaticFiles(directory=FX_FOLDER), name="static")


@app.get("/healthcheck")
def healthcheck():
    return "healthy"


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)


    def partition(list, n: int):
        """helper function to partition list into fixed-sized chunks"""
        # looping till length l
        for i in range(0, len(list), n):
            yield list[i:i + n]


    try:
        persistence_pool = [Persistence.from_environment().connect() for x in range(PERSISTENCE_POOL_SIZE)]


        def assign_persistence():
            return persistence_pool[randrange(PERSISTENCE_POOL_SIZE)]


        # phase 1: discover unprocessed files in directory
        for file in list_in_dir(FX_FOLDER):
            logging.info(f"saving unprocessed file path '{os.path.join(FX_FOLDER, file)}' to the database")
            assign_persistence().upsert_to_fx_files(folder=FX_FOLDER, filename=file)

        # phase 2: ingest into postgres timescaledb
        offset = 0
        while unprocessed := persistence_pool[0].fetch_unprocessed(offset=offset, limit=5):
            logging.info(f"fetched unprocessed page [{offset}]={unprocessed}")
            for entry in unprocessed:
                path = entry[0]
                logging.info(f"processing path={path}")
                try:
                    for batch in list(partition(list(read_oanda_streams_file(path)), BATCH_SIZE)):
                        persistence = assign_persistence()
                        persistence.insert_to_fx_prices(batch)
                except Exception as e:
                    logging.error(f"recovering from error {e.args}")
                marked = assign_persistence().mark_fx_file_processed(path)
                logging.info(f"path={marked} marked as successfully processed")
            offset += 1

    except Exception as e:
        logging.error(f"failed to ingest and mark unprocessed oanda market data, reason:{e.args}")
    finally:
        # dispose of persistent connection
        logging.info("system tear-down in progress")
