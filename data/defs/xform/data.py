def create_256(arr):
    """
    Method to create 3mm @ 256 x 256 slices

    """
    # --- Create box
    box = arr.new_box(0, 0, 0, 1, 1, 1)
    box.balance_aspect_ratio([None, 1, 1])
    
    # --- Create crop
    arr_ = arr.crop_and_resample(shape=(0, 256, 256), box=box)

    # --- Create mean IP 
    arr_ = arr_.create_mean_ip(thickness=3)

    return {'arr': arr_}

def create_crp(dat, lng):
    """
    Method to create volumes cropped to lungs 

    """
    crps = {}

    # --- Create box
    box = lng.find_bounds(padding=(0.05, 0.05, 0.05), acceleration=2)
    box.balance_aspect_ratio([None, 1, 1])
    
    # --- Create crop
    crps['dat'] = dat.crop_and_resample(shape=(0, 256, 256), box=box)
    
    # --- Create mean IP 
    crps['dat'] = crps['dat'].create_mean_ip(thickness=3)
    
    # --- Align 
    crps['lng'] = lng.align_with(crps['dat'], sigma=0.005)
    
    return crps 
