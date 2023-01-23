# %%
import h5py

hf = h5py.File('Data/annot_1.mat')
hf
# %%

# %%

dsobj = hf['annot']['patient']
dsobj
# %%
dsobj.len()
# %%
dsobj.shape
# %%
type(dsobj)
# %%
type(dsobj) == h5py.Dataset
# %%
ref = dsobj[0][0]
ref
# %%
deref = hf[ref]
deref
# %%
ndarr = deref[:]
ndarr
# %%
ndarr.tobytes().decode('utf-16')

# %%
def walk_root(hdf):
    root = hdf

    def walk_group(node):
        #print(f"{node}node type: {type(node)}")
        try:
            for kk in node.keys():
                walk_group(node[kk])
        except AttributeError:
            print(f"dataset: {node.dtype=}")
            
        return

    walk_group(root)

# %%
walk_root(hf)
L = ds.len()
print(f"len is {L}, {ds.shape=}")
print("attributes of ds:", list(ds.attrs.items()))

if L == 1:
    if type(ds) == h5py.Reference:
        print('found reference')
    # how do I know that this is a reference?
    ref = ds[0,0]
    print(f"{ref=}, {type(ref)}")
    deref = hf[ref]

    if type(deref) == h5py.Dataset:  # or has attribute dtype?
        print(f'{deref.dtype=}')
        if deref.dtype == np.uint16:
            arr = deref[:]
            print(f"{arr.dtype=}, {arr.shape=}")
            # if shape makes sense
            s = arr.tobytes().decode('utf-16')
            print(f'{s=}')
            
