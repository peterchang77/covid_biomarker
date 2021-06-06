import numpy as np
from jarvis.train.models import Trained
from jarvis.utils.arrays import blobs

# --- Load model
CODE = jtools.get_paths('covid_biomarker')['code']
trained = Trained(path='{}/data/defs/preds/pna/model.hdf5'.format(CODE))

def preprocess(dat):

    # --- Normalize
    dat = dat.clip(min=-1024, max=256) / 128 

    return dat 

def postprocess(logits, lng):

    pna = np.argmax(logits, axis=-1)
    pna = np.expand_dims(pna, axis=-1)
    pna[lng.data == 0] = 0
    
    return pna 

def predict(arr, lng):

    # --- Preprocess
    dat = preprocess(arr.data)
    
    # --- Predict
    ys = trained.run({'dat': dat}, softmax=True)

    # --- Postprocess
    pna = postprocess(ys['pna'], lng)

    # --- Create Jarvis array
    pna = arr.new_lbl(pna,
        group='lesion',
        label='pna')

    return {'pna': pna}
