import os.path
import logging
import psycopg2
from os import listdir
from os.path import isfile, join

def list_in_dir(dir):
    if not os.path.isdir(dir):
        raise RuntimeError("%s is not a directory" % dir)
    return [f for f in listdir(dir) if isfile(join(dir, f))]
