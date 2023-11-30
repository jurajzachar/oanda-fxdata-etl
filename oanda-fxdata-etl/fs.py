import gzip
import json
import logging
from json import JSONDecodeError
from os import listdir
from pathlib import Path
from typing import List, Generator, Optional
import os.path
from os.path import isfile, join

from pydantic import ValidationError

from oanda_schema import OandaPriceTick, unmarshall_from_wire


def list_in_dir(dir: str) -> List[str]:
    """ list all files in given directory """
    if not os.path.isdir(dir):
        raise RuntimeError(f"{dir} is not a directory")
    return [f for f in listdir(dir) if isfile(join(dir, f))]


def read_oanda_streams_file(file: str) -> Generator[Optional[OandaPriceTick], None, None]:
    path = Path(file)
    # sanity checks: file must exist and must be gzipped
    if not path.is_file():
        raise RuntimeError(f"File '{file}' does not exits")

    if not file.endswith(".gz"):
        raise RuntimeError(f"File '{file}' must be gzipped")

    with gzip.open(file) as f:
        for count, line in enumerate(f):
            try:
                data = json.loads(line)
                _type = data.get("type")
                # not interested in heartbeats
                if _type == "HEARTBEAT":
                    continue
                if _type == "PRICE":
                    try:
                        yield unmarshall_from_wire(data)
                    except ValidationError as e2:
                        logging.error(f'non-compliant price tick detected:{line}; {e2.args}')
                        yield None
            except JSONDecodeError as e1:
                # log and skip corrupt json objects
                logging.error(f'invalid json object detected:{line}; {e1.args}')
                continue
