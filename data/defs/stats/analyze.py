import numpy as np

def calculate_ratio(lng, pna, **kwargs):
    """
    Method to calculate ratios

    """
    outs = {}
    
    if type(lng) is str:
        return {}

    outs['vol-lng'] = lng.data.sum() * np.prod(lng.affine.extract_dims())
    outs['vol-pna'] = pna.data.sum() * np.prod(pna.affine.extract_dims())
    outs['ratio'] = outs['vol-pna'] / outs['vol-lng']

    return outs
