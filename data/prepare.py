import glob, os
import pandas as pd
from jarvis.utils.db import DB
from jarvis.utils.general import tools as jtools

DATA = jtools.get_paths('covid_biomarker')['data']

def create_symlinks(SRC, subdir='dcm'):

    DST = '{}/proc/{}'.format(DATA, subdir)
    srcs = glob.glob('{}/*'.format(SRC))

    for src in srcs:
        dst = '{}/{}'.format(DST, os.path.basename(src))
        print('Creating symlink: {}'.format(dst))
        if not os.path.exists(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            os.symlink(src=src, dst=dst)

def create_db_combined():

    # --- Initialize sids
    df = pd.read_csv('./csvs/raw_generic_xr_ct.csv')
    accs = set([str(s) for s in df['xr_accession']])

    # --- Create sids_xr 
    sids_xr = glob.glob('{}/proc/dcm/*/'.format(DATA))
    sids_xr = sorted([os.path.basename(s[:-1]) for s in sids_xr])
    sids_xr = [s for s in sids_xr if s in accs]

    # --- Create sids_ct
    xr_to_ct = {str(row['xr_accession']): str(row['ct_accession']) for n ,row in df.iterrows()}
    sids_ct = [xr_to_ct[s] for s in sids_xr]

    # --- Initialize fnames
    fnames = pd.DataFrame(index=sids_xr)

    # --- Original 
    fnames['dat-dcm-xr'] = ['{}/proc/dcm/{}/'.format(DATA, sid) for sid in sids_xr] 
    fnames['dat-dcm-ct'] = ['{}/proc/dcm/{}/'.format(DATA, sid) for sid in sids_ct] 
    fnames['dat-raw-xr'] = ['{}/proc/raw/{}/dat.hdf5'.format(DATA, sid) for sid in sids_xr] 
    fnames['dat-raw-ct'] = ['{}/proc/raw/{}/dat.hdf5'.format(DATA, sid) for sid in sids_ct] 

    # --- @ 256 (CT)
    fnames['dat-256-ct'] = ['{}/proc/256/{}/dat.hdf5'.format(DATA, sid) for sid in sids_ct]
    fnames['lng-256-ct'] = ['{}/proc/256/{}/lng.hdf5'.format(DATA, sid) for sid in sids_ct]

    # --- @ crp (CT)
    fnames['dat-crp-ct'] = ['{}/proc/crp/{}/dat.hdf5'.format(DATA, sid) for sid in sids_ct]
    fnames['lng-crp-ct'] = ['{}/proc/crp/{}/lng.hdf5'.format(DATA, sid) for sid in sids_ct]
    fnames['pna-crp-ct'] = ['{}/proc/crp/{}/pna.hdf5'.format(DATA, sid) for sid in sids_ct]

    # --- @ 512 (XR)
    fnames['dat-512-xr'] = ['{}/proc/512-512/{}/dat.hdf5'.format(DATA, sid) for sid in sids_xr]

    # --- @ 256 (XR)
    fnames['dat-256-xr'] = ['{}/proc/256-256/{}/dat.hdf5'.format(DATA, sid) for sid in sids_xr]

    # --- Initialize header 
    header = pd.DataFrame(index=sids_xr)
    header['vol-lng'] = ''
    header['vol-pna'] = ''
    header['ratio'] = ''

    # --- Create DB
    db = DB(
        project_id='covid_biomarker',
        prefix='db-generic-all',
        fnames=fnames,
        header=header)

    db.update_sform('{root}{curr}')

    db.to_yml()

def create_db(name='ct'):

    # --- Initialize sids
    df = pd.read_csv('./csvs/raw_covid_xr_ct.csv')
    accs = set(df['{}_accession'.format(name)])
    sevs = {row['{}_accession'.format(name)]: row['severity'] for n, row in df.iterrows()}

    # --- Find all sids matching current CSV file column
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
    header['vol-lng'] = ''
    header['vol-pna'] = ''
    header['ratio'] = ''

    # --- Create DB
    db = DB(
        project_id='covid_biomarker',
        prefix='db-{}-all'.format(name),
        fnames=fnames,
        header=header)

    db.sform = {}
    db.init_sform()

    db.to_yml()

# =============================================================================
# COMBINED: XR + CT (March 2020-21) 
# =============================================================================

# # --- Create links for XR (dcm + raw)
# create_symlinks('/home/chanon/caidm_DATA_prep/pna/xr_dcm', subdir='dcm')
# create_symlinks('/home/chanon/caidm_DATA_prep/pna/xr_raw', subdir='raw')
#
# # --- Create links for CT (dcm + raw + 256 + crp)
# create_symlinks('/home/chanon/caidm_DATA_prep/pna/proc/dcm', subdir='dcm')
# create_symlinks('/home/chanon/caidm_DATA_prep/pna/proc/raw', subdir='raw')
# create_symlinks('/home/chanon/caidm_DATA_prep/pna/proc/256', subdir='256')
# create_symlinks('/home/chanon/caidm_DATA_prep/pna/proc/crp', subdir='crp')

# --- Create DB
# create_db_combined()

# =============================================================================
# COVID: CT
# =============================================================================

# --- Create links
# create_symlinks(SRC='/home/chanon/seriesid/covid_chestct_master-06-2021_filtered_dcms')

# --- Create DB
# create_db()

# =============================================================================
# COVID: XR (TODO)
# =============================================================================
