# coding: utf-8
import sys
import pandas as pd
import numpy as np

IN  = sys.argv[1]
OUT = sys.argv[2]

with open(IN, "r") as f:
    fa = [a.strip() for a in f.readlines()]
fb = np.array (fa)
ifb = fb.reshape ((-1, 3)).T
df = pd.DataFrame({'fname':ifb[0], 'line1':ifb[1], 'line2':ifb[2]})
# df['name'] = df.fname.apply (lambda x : x[2:])
df['name'] = df.fname
df.drop (columns='fname', inplace=True)
df.to_pickle(OUT)
