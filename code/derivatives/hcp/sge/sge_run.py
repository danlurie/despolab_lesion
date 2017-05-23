import sys
import os
import numpy as np
import pandas as pd
import nibabel as nib
from nilearn import input_data

subid = sys.argv[1]

hp200_clean_wbsreg = '/home/despoB/connectome-data/{0}/rfMRI_REST1_LR/rfMRI_REST1_LR_hp2000_clean_wbsreg.nii.gz'.format(subid)
brainmask_fs = nib.load('/home/despoB/connectome-raw/{0}/MNINonLinear/Results/rfMRI_REST1_LR/brainmask_fs.2.nii.gz'.format(subid))
BNA_2mm = '/home/despoB/dlurie/Data/reference/Brainnetome/BNA-maxprob-thr25-2mm.nii.gz'

ts_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/control_data/hcp/sub-{0}/func/sub-{0}_task-rest_acq-LR_run-01_bold_space-MNI_timeseries_atlas-BNA_wbsreg.npy'
corrmat_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/control_data/hcp/sub-{0}/func/sub-{0}_task-rest_acq-LR_run-01_bold_space-MNI_corrmat_atlas-BNA_wbsreg.npy'

bna_img = nib.load(BNA_2mm)

os.makedirs('/home/despoB/dlurie/Projects/despolab_lesion/control_data/hcp/sub-{0}/func'.format(subid))

bna_masker = input_data.NiftiLabelsMasker(labels_img=bna_img, background_label=0, mask_img=brainmask_fs,
                                          standardize=False,  detrend=False, low_pass=0.2, high_pass=0.01, t_r=0.720,
                                          resampling_target="data")

print("...extracting brainnetome timeseries for subject {0}...".format(subid))
timeseries = bna_masker.fit_transform(hp200_clean_wbsreg)
np.save(ts_fpt.format(subid), timeseries)

print("...computing correlation matrix for subject {0}...".format(subid))
corrmat = np.corrcoef(timeseries.T)
np.save(corrmat_fpt.format(subid), corrmat)
