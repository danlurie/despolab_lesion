import numpy as np
import pandas as pd
import nibabel as nib
from nilearn import image

def epi_atlas_coverage(brain_mask, atlas):
    atlas_img = nib.load(atlas)
    mask_img = nib.load(brain_mask)
    atlas_resample = image.resample_to_img(atlas_img, mask_img, interpolation='nearest')
    mask_data = mask_img.get_data()
    atlas_data = atlas_resample.get_data()
    coverage_data = mask_data*atlas_data
    roi_labels = np.unique(atlas_data)
    
    roi_sizes = []
    for roi in roi_labels:
        roi_sizes.append(np.count_nonzero(atlas_data == roi))
    
    roi_coverage = []
    for roi in roi_labels:
        roi_coverage.append(np.count_nonzero(coverage_data == roi))
    
    df = pd.DataFrame.from_records(np.array([roi_sizes, roi_coverage]).T, columns=['roi_size', 'roi_count'])
    df = df.set_index(roi_labels.astype('uint16')) 
    df.loc[:,'pct_cov'] = df['roi_count']/df['roi_size']*100
    df.index.name = 'roi_label'
    return df


for acq in ['128px', '64px']:
    # Load list of subjects with the specified EPI sequence.
    sublist_file = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/meta/has_acq-{0}.txt'.format(acq)
    subject_list = np.loadtxt(sublist_file, dtype='int')
    subject_list = [str(i) for i in subject_list]

    print("Processing {0} patients who were scanned with the {1} sequence...".format(str(len(subject_list)), acq))

    # Set file path templates
    mask_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/preproc/out/fmriprep/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_space-T1w_brainmask.nii.gz'
    atlas_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/sub-{0}/anat/sub-{0}_t1w_label-AAL2_atlas.nii.gz'
    out_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_space-T1w_atlas-AAL2_mask-brainmask_EPIcoverage.csv'

    for pid in subject_list:
        atlas_path = atlas_fpt.format(pid)
        brainmask_path = mask_fpt.format(pid,acq)
        print('Calculating EPI coverage for patient {0}...'.format(pid))
        df = epi_atlas_coverage(brainmask_path, atlas_path)
        print('Saving EPI coverage data for patient {0}...'.format(pid))
        out_path = out_fpt.format(pid,acq)
        df.to_csv(out_path) 
