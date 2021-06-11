import numpy as np
from jarvis.utils.db import DB
from jarvis.utils import arrays as jars

def create_all_generic(yml='./ymls/db-generic-all.yml'):

    db = DB(yml, load=jars.create)

    # --- Manual (serial)
    # db.refresh(cols='dat-raw-xr', flush=True)
    # db.refresh(cols='dat-512-xr', flush=True, skip_existing=False)

def create_all_covid(yml='./ymls/db-ct-all.yml'):

    db = DB(yml, load=jars.create)

    # --- Manual (serial)
    # db.refresh(cols='dat-raw', flush=True)
    # db.refresh(cols='dat-256', flush=True)
    # db.refresh(cols='lng-256', flush=True)
    # db.refresh(cols='dat-crp', flush=True)
    # db.refresh(cols='pna-crp', flush=True)

    # --- Stats
    # db.refresh(cols='ratio', flush=True)
    # db.to_csv()

# ===============================================================================
# create_all_generic()
# create_all_covid()
# ===============================================================================
