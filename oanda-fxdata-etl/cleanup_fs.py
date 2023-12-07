import logging

from config import FX_FOLDER, FX_LONG_TERM_STORAGE
from db import Persistence
from fs import move_file_to_dir


def move_all_processed_files_to_long_term_storage(pers: Persistence):
    offset = 0
    while processed := pers.fetch_processed(offset=offset, limit=10):
        logging.info(f"fetched processed page [{offset}]={processed}")
        for entry in processed:
            path = entry[0]
            try:
                move_file_to_dir(path, FX_FOLDER, FX_LONG_TERM_STORAGE)
                logging.info(f"successfully processed path={path}")
            except Exception as e:
                logging.warning(f"ignoring path='{path}'; reason={e.args}")

        offset += 1


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
    persistence = Persistence.from_environment().connect()
    move_all_processed_files_to_long_term_storage(persistence)
