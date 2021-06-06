import numpy as np
from jarvis.train.models import Trained
from jarvis.utils.arrays import blobs
from jarvis.utils.general import tools as jtools

# --- Load model
CODE = jtools.get_paths('covid_biomarker')['code']
trained = Trained(path='{}/data/defs/preds/lung/model.hdf5'.format(CODE))
    
def preprocess(dat):

    # --- Normalize
    dat = dat.clip(min=-1024, max=256) / 128 

    return dat 

def postprocess(logits):

    msk = np.argmax(logits, axis=-1)
    msk = blobs.find_largest(msk, n=2)

    return msk 

def predict(arr):

    # --- Preprocess
    dat = preprocess(arr.data)
    
    # --- Predict
    ys = trained.run({'dat': dat}, softmax=True)

    # --- Postprocess
    lng = postprocess(ys['lbl'])

    # --- Create Jarvis array
    lng = arr.new_lbl(lng,
        group='anatomy',
        label='lung')

    return {'lng': lng}
