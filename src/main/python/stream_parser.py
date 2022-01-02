import logging, fileinput, time, json
from typing import NamedTuple
from pathlib import Path

def read_oanda_streams_file(file):
    path = Path(file)
    if not path.is_file():
        raise RuntimeError("File '%s' does't exits" % file)
    start = time.time()
    count_lines = 0
    count_heartbeats = 0
    count_ticks = 0
    data = []
    for line in fileinput.input([file]):
        count_lines += 1
        # parse into json
        try:
            fragment = json.loads(line)
            if fragment["type"] == "HEARTBEAT":
                count_heartbeats += 1
            elif fragment["type"] == "PRICE":
                count_ticks += 1
                data.append(fragment)
            else:
                raise RuntimeError("unknown data type: %s" % fragment)

        except:
            logging.warning("skipping malformed json: %s" % line)

    end = time.time()

    return (data, ExecOutput(count_lines, count_heartbeats, count_ticks, (end-start)))

class ExecOutput(NamedTuple):
    no_of_lines: int
    no_of_heartbeats: int
    not_of_ticks: int
    read_time: float