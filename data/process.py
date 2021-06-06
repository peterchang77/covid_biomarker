import numpy as np
from jarvis.utils.db import DB
from jarvis.utils import arrays as jars

def create_all(yml='./ymls/db-ct-all.yml'):

    db = DB(yml, load=jars.create)

    # --- Manual (serial)
    db.refresh(cols='dat-raw', flush=True)

    db.refresh(cols='dat-256', flush=True)
    db.refresh(cols='lng-256', flush=True)

    db.refresh(cols='dat-crp', flush=True)
    db.refresh(cols='pna-crp', flush=True)

    db.refresh(cols='ratio', flush=True)

# ===============================================================================
# create_all()
# ===============================================================================
