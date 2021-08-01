# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.3
#   kernelspec:
#     display_name: 'Python 3.8.10 64-bit (''mne'': conda)'
#     name: python3
# ---

# %%
import yaml
import json
import glob
import itertools 
import random

import scipy.io as sio
import h5py
import mat4py # even more convenient that scipy.io.loadmat for v5
import numpy as np

# %%
#asbytes_latin1 = lambda s: s.encode('latin1') # may want utf-8
#asstr_latin1 = lambda b: b.decode('latin1')

asbytes_latin1 = lambda s: s.encode('utf-8') # may want utf-8
asstr_latin1 = lambda b: b.decode('utf-8')

def ndarray_uint16_to_string(arr):
    arr_uint = arr.astype('uint8') # truncate off 2nd byte
    arr_bytes = arr_uint.tobytes()
    return asstr_latin1(arr_bytes)



# %%
annotation_files = glob.glob('a*.mat')

# %%
annotation_files.sort()


# %%
ann = {}
errorfiles = []

for afile in annotation_files:
    sp = afile.split('_')
    num_str = sp[1][:-4]
    annot_name = afile[:-4]
    num = int(num_str)
    #print(f"working on {annot_name=} {num} from file {afile}")
    try:
        h = h5py.File(afile)
        
        #print(f"{list(h.keys())}")
        a = h[annot_name]
        datasets = {}
        for kk,vv  in a.items():
            #print(f"{kk}: {vv[:]=}")
            datasets[kk] = vv[:]
        ann[num] = datasets 
       
    except OSError:
        print(f"problems opening {afile}")
        errorfiles.append(afile) 
    

    #h = h5py.File(afile)

# %%
len(ann)

# %%
# fix those annotations
for kk, aa in ann.items():
    for jj, vv in aa.items():
        aa[jj] = np.squeeze(vv)
    aa['patient'] = ndarray_uint16_to_string(aa['patient'])


# %%

# %%

# random_annotation = random.choice(ann)
# %%
#random_annotation['patient']

# %%
for fn in errorfiles:
    sp = fn.split('_')
    num_str = sp[1][:-4]
    annot_name = fn[:-4]
    num = int(num_str)
    print(f"{fn=},{num=}, {annot_name=}")
    data = mat4py.loadmat(fn)
    print(data)
    ann[num] = data[annot_name] 


# %%
# now we may as well convert things to python lists given how short these arrays are

for kk in ann:
    data = ann[kk]
    for ii,vv in data.items():
        if type(vv) == np.ndarray:
            data[ii] = vv.tolist()


# %%
for kk, data in ann.items():
    for ii,vv in data.items():
        if type(vv) == list:
            data[ii] = [int(val) for val in vv]
        if type(vv) == float:
            data[ii] = [int(vv)]  # make it so that they are always a list


# %%
# %% [markdown]
# #### reading through pull_data.m
# ii_start and ii_stop are related to interictal start and stop timesince
# ```
# for files with seizures (type=1)
# when not given, the dataset acquistions times are inferred
#
# dataset_start is the minimum of (ii_start, ii_stop, sz_start, sz_stop)
# dataset_stop = max(ii_start, ii_stop, sz_start, sz_stop)
#
# for type==2, seizure free patient files
# there are again interictal start/stop times ii_start and ii_stop
#
# and the dataset_start/stop are ii_start/ii_stop 

# type ==3 is for the "IIC" or interictal continuum patients 
# ```

# ## Important
# the mat v5 files do not contain data start/stop annotations
# %%

from collections.abc import Iterable
gen_flatten = lambda *n: (e for a in n
                            for e in (gen_flatten(*a) if isinstance(a, Iterable) else (a,)))

def flatten_list(*l):
    return list(gen_flatten(*l))

# %%
for kk, an in ann.items():
    if 'type' not in an:
        print(f"{kk=}, {an=} does not have a type")
        continue 
    # check
    present_keys = [ss for ss in ['iic_start','iic_stop','ii_start','ii_stop',
                        'sz_start', 'sz_stop'] if ss in an]
    check_list = [an[ss] for ss in present_keys]
    print(f"{check_list=}")

    check_these = flatten_list(check_list) # flatten
    allarr = np.array(check_these)
    if an['type'] == 1: # seizure file
        if 'data_start' not in an:
            an['data_start'] = np.min(allarr)
        if 'data_stop' not in an:
            an['data_stop'] = np.max(allarr)
    elif an['type'] == 2: # seizure free
        if 'data_start' not in an:
            #an['data_start'] = np.min(min(an['ii_start']), min(an['ii_stop']) )
            an['data_start'] = np.min(allarr )
        if 'data_stop' not in an:
            #an['data_stop'] = np.max([ max(an['ii_start']), max(an['ii_stop'])])
            an['data_stop'] = np.max(allarr)
    elif an['type'] == 3: # interictal continuum
        if 'data_start' not in an:
            #an['data_start'] = np.min((min(an[ss]) for ss in check_these) )
            an['data_start'] = np.min(allarr)
        if 'data_stop' not in an:
            #an['data_stop'] = np.max(max(an[ss]) for ss in check_these)
            an['data_stop'] = np.max(allarr)

# %%
# little test
tst = {'a': [1,3,5],
'b': [3, 4,7]}
check_this = [ss for ss in ['a','b','c'] if ss in tst]
check_this
# %%


# %%
yaml.safe_dump(ann, open('annotations.yaml','w+'))


# %%
json.dump(ann, open('annotations.json', 'w+'), indent='\t')

# %%
