import os
import sys

project_path = os.getcwd()
source_path = os.path.join(
    project_path,"oanda-fxdata-etl"
)
sys.path.append(source_path)