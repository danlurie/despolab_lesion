"""
Create symlinks in ../mask_prep/combined to point to the actual mask files
which live in ../mask_prep/old_masks and ../mask_prep/new_masks.

If a patient has both and old and a new mask, use the new mask.

For each set (has_old, has_new, etc), write a list of patients.
"""
import os
import glob

old_wcard = '/home/despoB/lesion/mask_prep/old_masks/*/*_lesion_mask_bin_dereg_padded_AIL.nii.gz'
old_masks = sorted(glob.glob(old_wcard))
has_old = [os.path.basename(fpath)[0:3] for fpath in old_masks]

with open('has_old_mask.txt', 'w') as outf:
    for pid in has_old:
        outf.write(pid)
        outf.write('\n')

new_dir = '/home/despoB/lesion/mask_prep/new_masks/'
new_masks = sorted(os.listdir(new_dir))
has_new = [os.path.basename(fpath)[0:3] for fpath in new_masks]

with open('has_new_mask.txt', 'w') as outf:
    for pid in has_new:
        outf.write(pid)
        outf.write('\n')

new_set = set(has_new)
old_set = set(has_old)

has_both = sorted(list(new_set.intersection(old_set)))

with open('has_old_and_new_mask.txt', 'w') as outf:
    for pid in has_both:
        outf.write(pid)
        outf.write('\n')

old_only = sorted(list(old_set - new_set))

with open('has_old_mask_only.txt', 'w') as outf:
    for pid in old_only:
        outf.write(pid)
        outf.write('\n')

old_fpt = '/home/despoB/lesion/mask_prep/old_masks/{0}/{0}_lesion_mask_bin_dereg_padded_AIL.nii.gz'
combined_fpt = '/home/despoB/lesion/mask_prep/combined/{}_manual_mask.nii.gz'

for pid in old_only:
    fpath = old_fpt.format(pid)
    lpath = combined_fpt.format(pid)
    os.symlink(fpath, lpath)

for fname in new_masks:
    pid = fname[0:3]
    fpath = os.path.join(new_dir, fname)
    lpath = combined_fpt.format(pid)
    os.symlink(fpath, lpath)

