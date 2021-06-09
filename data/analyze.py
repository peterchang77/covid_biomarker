import numpy as np
from jarvis.utils.db import DB
from matplotlib import pyplot
import scipy.optimize as opt

def curve(x, a, b, c):
     return a * x ** 2 + b * x + c 

def plot_ratio_severity(yml='./ymls/db-ct-all.yml'):

    db = DB(yml)

    # --- Extract severity and ratio
    e = db.exists(['pna-crp'], ret=True)['pna-crp']
    s = np.array(db.header['severity'][e], dtype='float32')
    r = np.array(db.header['ratio'][e], dtype='float32')

    ratios = np.arange(0, 1, 0.025)

    pyplot.clf()
    fig = pyplot.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)

    for severity in sorted(set(s))[:-1]:
        ys, xs = [], []
        s_ = s <= severity
        for ratio in ratios:
            m = r >= ratio
            if m.any():
                xs.append(ratio)
                ys.append(sum(m & s_) / sum(m))

        # --- Plot
        xs = np.array(xs)
        ys = np.array(ys)
        ax.scatter(xs, ys, marker='.')
        optimizedParameters, pcov = opt.curve_fit(curve, xs, ys);
        ax.plot(xs, curve(xs, *optimizedParameters))

    ax.set_title('Outcomes Stratified by Lung Injury Score')
    ax.set_xlabel('Lung Injury Score')
    ax.set_ylabel('Probability (%)')
    ax.legend(['Death', 'ICU (intubated)', 'ICU (non-intubated)', 'IP (HF)', 'IP (NC)', 'IP (no O2)'])
    pyplot.savefig('./pngs/ratio_severity.png')

# ===============================================================================
# plot_ratio_severity()
# ===============================================================================
