import numpy as np
import pandas as pd
import nibabel as nib

def atlas_lesion_damage(lesion_mask, atlas):
    atlas_img = nib.load(atlas)
    atlas_data = atlas_img.get_data()
    lesion_img = nib.load(lesion_mask)
    lesion_data = lesion_img.get_data()
    
    coverage_data = lesion_data*atlas_data
    roi_labels = np.unique(atlas_data)
    
    roi_sizes = []
    for roi in roi_labels:
        roi_sizes.append(np.count_nonzero(atlas_data == roi))
    
    roi_coverage = []
    for roi in roi_labels:
        roi_coverage.append(np.count_nonzero(coverage_data == roi))
    
    df = pd.DataFrame.from_records(np.array([roi_sizes, roi_coverage]).T, columns=['roi_size', 'lesioned_vox'])
    df = df.set_index(roi_labels.astype('uint16')) 
    df.loc[:,'pct_lesion'] = df['lesioned_vox']/df['roi_size']*100
    df.index.name = 'roi_label'
    return df

# Load list of subjects
sublist_file = '/home/despoB/dlurie/Projects/despolab_lesion/code/preproc/mask_prep/has_bids_mask.txt'
subject_list = np.loadtxt(sublist_file, dtype='int')
subject_list = [str(i) for i in subject_list]

atlas_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/sub-{0}/anat/sub-{0}_t1w_label-AAL2_atlas.nii.gz'
lesion_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/sub-{0}/anat/sub-{0}_t1w_variant-reorient_label-lesion_roi.nii.gz'
out_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/sub-{0}/anat/sub-{0}_t1W_atlas-AAL2_mask-lesion_ROIdamage.csv'

for pid in subject_list:
    try:
        atlas_path = atlas_fpt.format(pid)
        lesion_path = lesion_fpt.format(pid)
        print('Calculating ROI damage for patient {0}...'.format(pid))
        df = atlas_lesion_damage(lesion_path, atlas_path)
        print('Saving ROI damage data for patient {0}...'.format(pid))
        out_path = out_fpt.format(pid)
        df.to_csv(out_path)
    except:
        print('ERROR!')
        pass
