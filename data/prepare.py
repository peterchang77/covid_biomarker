import glob, os
import pandas as pd
from jarvis.utils.db import DB
from jarvis.utils.general import tools as jtools

DATA = jtools.get_paths('covid_biomarker')['data']

def create_symlinks(SRC='/home/chanon/seriesid/covid_chestct_master-06-2021_filtered_dcms'):

    DST = '{}/proc/dcm'.format(DATA)
    srcs = glob.glob('{}/*'.format(SRC))

    for src in srcs:
        dst = '{}/{}'.format(DST, os.path.basename(src))
        print('Creating symlink: {}'.format(dst))
        if not os.path.exists(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            os.symlink(src=src, dst=dst)

def create_db(name='ct'):

    # --- Initialize sids
    df = pd.read_csv('./csvs/covid_biomarker.csv')
    accs = set(df['{}_accession'.format(name)])
    sevs = {row['{}_accession'.format(name)]: row['severity'] for n, row in df.iterrows()}

    sids = glob.glob('{}/proc/dcm/*/'.format(DATA))
    sids = sorted([os.path.basename(s[:-1]) for s in sids])
    sids = [s for s in sids if s in accs]

    # --- Initialize fnames
    fnames = pd.DataFrame(index=sids)

    # --- Original 
    fnames['dat-dcm'] = ''
    fnames['dat-raw'] = ''

    # --- @ 256
    fnames['dat-256'] = ''
    fnames['lng-256'] = ''

    # --- @ crp
    fnames['dat-crp'] = ''
    fnames['lng-crp'] = ''
    fnames['pna-crp'] = ''

    # --- Initialize header 
    header = pd.DataFrame(index=sids)
    header['severity'] = [sevs[s] for s in sids]
    header['vol-lng'] = 0
    header['vol-pna'] = 0
    header['ratio'] = 0

    # --- Create DB
    db = DB(
        project_id='covid_biomarker',
        prefix='db-{}-all'.format(name),
        fnames=fnames,
        header=header)

    db.init_sform()

    db.to_yml()

# =============================================================================
# create_symlinks()
# create_db()
# =============================================================================
