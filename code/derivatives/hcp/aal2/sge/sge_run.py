import sys
import os
import numpy as np
import pandas as pd
import nibabel as nib
from nilearn import input_data

subid = sys.argv[1]

hp200_clean_wbsreg = '/home/despoB/connectome-data/{0}/rfMRI_REST1_LR/rfMRI_REST1_LR_hp2000_clean_wbsreg.nii.gz'.format(subid)
brainmask_fs = nib.load('/home/despoB/connectome-raw/{0}/MNINonLinear/Results/rfMRI_REST1_LR/brainmask_fs.2.nii.gz'.format(subid))
AAL2 = '/home/despoB/dlurie/Data/reference/AAL/AAL2_MNI_V5.nii'

ts_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/data/hcp/derivatives/sub-{0}/func/sub-{0}_task-rest_acq-LR_run-01_bold_space-MNI_variant-wbsreg_atlas-AAL2_timeseries.npy'
corrmat_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/data/hcp/derivatives/sub-{0}/func/sub-{0}_task-rest_acq-LR_run-01_bold_space-MNI_variant-wbsreg_atlas-AAL2_corrmat.npy'

aal2_img = nib.load(AAL2)

out_dir = '/home/despoB/dlurie/Projects/despolab_lesion/data/hcp/derivatives/sub-{0}/func'.format(subid)

if os.path.isdir(out_dir) is False:
    os.makedirs(out_dir)

aal2_masker = input_data.NiftiLabelsMasker(labels_img=aal2_img, background_label=0, mask_img=brainmask_fs,
                                          standardize=False,  detrend=False, low_pass=0.2, high_pass=0.01, t_r=0.720,
                                          resampling_target="data")

print("...extracting AAL2 timeseries for subject {0}...".format(subid))
timeseries = aal2_masker.fit_transform(hp200_clean_wbsreg)
np.save(ts_fpt.format(subid), timeseries)

print("...computing correlation matrix for subject {0}...".format(subid))
corrmat = np.corrcoef(timeseries.T)
np.save(corrmat_fpt.format(subid), corrmat)
