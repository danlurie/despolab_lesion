"""
Creates symlinks in the ../data/original/bids directory that point to the actual
mask files which currently (as of May 2017) live in ../lesion/mask_prep/clean
"""
 
import os

clean_fpt = '/home/despoB/lesion/mask_prep/clean/{0}_clean_mask.nii.gz'
bids_fpt = '/home/despoB/lesion/data/original/bids/sub-{0}/anat/sub-{0}_t1w_label-lesion_roi.nii.gz' 

clean_masks = os.listdir('/home/despoB/lesion/mask_prep/clean/')

# Create symlinks
for fname in clean_masks:
    try:
        pid = fname[0:3]
        cpath = clean_fpt.format(pid)
        bpath = bids_fpt.format(pid)
        os.symlink(cpath, bpath)
        print('BIDS symlink created for patient '+pid)
    except:
        print('Error creating symlink for patient '+pid)
        pass

# Write a list of patients with BIDS masks
has_bids_mask = sorted([i[0:3] for i in clean_masks])
with open('has_bids_mask.txt', 'w') as outf:
    for pid in has_bids_mask:
        outf.write(pid)
        outf.write('\n')
