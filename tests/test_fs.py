import os.path
import unittest
from os import path

import pytest

from fs import read_oanda_streams_file
from oanda_schema import OandaPriceTick


@pytest.fixture
def local_fixture(request):
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "fixtures/file.json.gz")


def test_should_parse_valid_lines(local_fixture):
    output = list(read_oanda_streams_file(local_fixture))
    assert 2 == len(output), "expected number tick prices doesn't match"
    for elem in output:
        assert isinstance(elem, OandaPriceTick)
