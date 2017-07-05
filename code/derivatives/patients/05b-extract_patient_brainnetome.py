import numpy as np
import pandas as pd
import nibabel as nib
from nilearn import input_data

def extract_brainnetome(epi_acq):
    # Load list of subjects with the specified EPI sequence.
    sublist_file = '/home/despoB/dlurie/Projects/despolab_lesion/derivatives/has_acq-{0}.txt'.format(epi_acq)
    subject_list = np.loadtxt(sublist_file, dtype='int')
    subject_list = [str(i) for i in subject_list]

    print("Processing {0} patients who were scanned with the {1} sequence...".format(str(len(subject_list)), epi_acq))

    # Set file path templates
    func_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/preproc/out/fmriprep/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_space-T1w_preproc.nii.gz'
    mask_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/preproc/out/fmriprep/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_space-T1w_brainmask.nii.gz'
    atlas_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/derivatives/sub-{0}/anat/sub-{0}_t1w_label-BNA_atlas.nii.gz'
    motion24_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/derivatives/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_confounds-motion24.csv'
    ts_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/derivatives/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_space-T1w_timeseries_atlas-BNA_motion24.npy'
    corrmat_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/derivatives/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_space-T1w_corrmat_atlas-BNA_motion24.npy'

    for pid in subject_list:

        bold_T1w_preproc = func_fpt.format(pid,epi_acq)
        bold_T1w_brainmask = nib.load(mask_fpt.format(pid,epi_acq))
        atlas_T1w_BNA = atlas_fpt.format(pid)
        confounds = motion24_fpt.format(pid,epi_acq)

        bna_img = nib.load(atlas_T1w_BNA)

        bna_masker = input_data.NiftiLabelsMasker(labels_img=bna_img, background_label=0, mask_img=bold_T1w_brainmask,
                                                  standardize=False,  detrend=True, low_pass=0.2, high_pass=0.01, t_r=2,
                                                  resampling_target="data")

        print("...extracting brainnetome timeseries for patient {0}...".format(pid))
        timeseries = bna_masker.fit_transform(bold_T1w_preproc, confounds)
        np.save(ts_fpt.format(pid,epi_acq), timeseries)
    
        print("...computing correlation matrix for patient {0}...".format(pid))
        corrmat = np.corrcoef(timeseries.T)
        np.save(corrmat_fpt.format(pid,epi_acq), corrmat)


for acq in ['128px', '64px']:
    extract_brainnetome(acq)
