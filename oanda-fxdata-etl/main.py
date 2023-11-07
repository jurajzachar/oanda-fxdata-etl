import logging
import os
from db import Persistence
from oanda_filesystem import *
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# prod: '/oxygen/oanda-streams'
FX_FOLDER = os.getenv('fx_folder', '/oxygen/oanda-streams')
app = FastAPI()
app.mount("/static", StaticFiles(directory=FX_FOLDER), name="static")

@app.get("/healthcheck")
def healthcheck():
    return "healthy"


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

    # discover files in dir and dump them to db
    persistence = Persistence()
    try:
        persistence.connect()
        for file in list_in_dir(FX_FOLDER):
            logging.info("saving '%s' to the db", join(FX_FOLDER, file))
            persistence.upsert_to_db(folder=FX_FOLDER, filename=file)
    except Exception as e:
        logging.error("failed ingest raw Oanda FX files ")
    finally:
        # dispose of persistent connection
        logging.info("system tear-down in progress")
