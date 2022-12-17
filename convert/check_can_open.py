# kernel pyt181 (lts)
# %%
import glob
import pathlib
import h5py
# %%
allmat = glob.glob('*.mat')


for fn in allmat:
    try:
        hf = h5py.File(fn)
        print(list(hf.items()))
    except:
        print(f"failed to open {fn}")

# results, all .mat files could be opened with hf        
