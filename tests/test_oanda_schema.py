import logging
import os.path

import pytest
import json

from oanda_schema import unmarshall_from_wire

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

@pytest.fixture
def local_fixture(request):
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "fixtures/oanda_streams_sample.json")

def test_should_unmarshall_from_wire(local_fixture):
    objects = []
    with open(local_fixture, 'r') as file:
        for count, line in enumerate(file):
            try:
                data = json.loads(line)
                model = unmarshall_from_wire(data)
                if model is not None:
                    objects.append(model)
            except Exception as e:
                # suppress, some files are expected to contain corrup lines
                pass
    assert len(objects) == 2