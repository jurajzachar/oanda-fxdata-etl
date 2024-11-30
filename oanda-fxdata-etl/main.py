import logging
import threading
from concurrent.futures import ThreadPoolExecutor

import config
from config import *
from db import Persistence

from fs import list_in_dir, read_oanda_streams_file


def process_file(entry):
    path = entry[0]

    logging.info(f"[Thread-{threading.get_ident()}] processing path={path} ...")
    with Persistence.from_environment() as p:
        try:

            for batch in list(partition(list(read_oanda_streams_file(path)), BATCH_SIZE)):
                p.insert_to_fx_prices(batch)

            marked = p.mark_fx_file_processed(path)
            logging.info(f"[Thread-{threading.get_ident()}] path={marked} marked as successfully processed")
        except Exception as persistenceError:
            logging.error(f"recovering from error {persistenceError.args}")
            logging.warning(f"skipping batch: {batch}")
    return 1


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s:\n %(message)s', level=logging.INFO)

    max_workers = config.CPU_COUNT

    def partition(l, n: int):
        """helper function to partition list into fixed-sized chunks"""
        # looping till length l
        for i in range(0, len(l), n):
            yield l[i:i + n]


    try:
        # phase 1: discover unprocessed files in directory
        for file in list_in_dir(FX_FOLDER):
            logging.info(f"saving unprocessed file path '{os.path.join(FX_FOLDER, file)}' to the database")
            with Persistence.from_environment() as persistence:
                persistence.upsert_to_fx_files(folder=FX_FOLDER, filename=file)

        # phase 2: ingest into postgres timescaledb
        with Persistence.from_environment() as persistence:
            unprocessed = persistence.fetch_all_unprocessed()
            logging.info(f"fetched unprocessed files {len(unprocessed)}")
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                executor.map(process_file, unprocessed)

    except Exception as e:
        logging.error(f"failed to ingest and mark unprocessed oanda market data, reason:{e.args}")
    finally:
        # dispose of persistent connection
        logging.info("system tear-down in progress")
