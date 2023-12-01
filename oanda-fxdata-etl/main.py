import logging
import os.path

from db import Persistence
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fs import list_in_dir

FX_FOLDER = '/oxygen/oanda-streams'
app = FastAPI()
app.mount("/static", StaticFiles(directory=FX_FOLDER), name="static")

@app.get("/healthcheck")
def healthcheck():
    return "healthy"


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

    # discover files in dir and dump them to db
    persistence = Persistence.from_environment()
    try:
        persistence.connect()
        for file in list_in_dir(FX_FOLDER):
            logging.info(f"saving unprocessed file path '{os.path.join(FX_FOLDER, file)}' to the database")
            persistence.upsert_to_fx_files(folder=FX_FOLDER, filename=file)
    except Exception as e:
        logging.error(f"failed mark unprocessed oanda market data, reason:{e.args}")
    finally:
        # dispose of persistent connection
        logging.info("system tear-down in progress")
        persistence.__del__()
