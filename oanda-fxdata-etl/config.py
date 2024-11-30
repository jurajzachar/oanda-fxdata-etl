import os

FX_FOLDER = os.environ.get('fx_folder', '/oxygen/oanda-streams')
FX_LONG_TERM_STORAGE = os.environ.get('fx_long_store', '/hydrogen/oanda-streams')
# fx_prices ingestion
BATCH_SIZE = 1000
CPU_COUNT = int(os.environ.get('cpu_count', 4))
