"""
De-register lesion masks drawn by Emi/Caterina. These were drawn on a "cut"
T1 image which had been registered to EPI space. We want them in raw T1 space.

This script deals with two subjects in the ../extra_subs directory.
"""

import os
import shutil
import subprocess

WORKING_DIR = '/home/despoB/lesion/mask_prep/old_masks'
subject_list = ['153','154']


for sub_id in subject_list:
    # Define input paths.
    subject_data_dir = '/home/despo/rstate/data/Rest.Lesion/Data/extra_subs/{}/Rest'.format(sub_id)

    # Get the T1-Cut image paths.
    if sub_id in ['104']:
        t1_cut_orig = os.path.join(subject_data_dir, '{}-T1-Cut_OLDDATA.nii.gz'.format(sub_id))
    elif sub_id in ['108']:
        t1_cut_orig = os.path.join(subject_data_dir, '{}-T1-Cut-shift_OLDFILE.nii.gz'.format(sub_id))
    elif sub_id in ['113','133','136','140']:
        t1_cut_orig = os.path.join(subject_data_dir, '{}-T1-Cut_OLDFILE.nii.gz'.format(sub_id))
    elif sub_id in ['131']:
        t1_cut_orig = os.path.join(subject_data_dir, '{}-T1-Cut_nudge_OLDFILE.nii.gz'.format(sub_id))
    elif sub_id in ['150','151','152','154']:
        t1_cut_orig = os.path.join(subject_data_dir, '{}-T1-Cut_nudge.nii.gz'.format(sub_id))
    elif sub_id in ['161']:
        t1_cut_orig = os.path.join(subject_data_dir, '{}-T1-Cut-manualacpc.nii.gz'.format(sub_id))
    else:
        t1_cut_orig = os.path.join(subject_data_dir, '{}-T1-Cut.nii.gz'.format(sub_id))

    t1_cut_coreg_orig = os.path.join(subject_data_dir, '{}-T1-Cut-CoReg.nii.gz'.format(sub_id))
    xfm_orig = os.path.join(subject_data_dir, '{}-T1-Cut.nii_al_mat.aff12.1D.gz'.format(sub_id))

    # Get the lesion mask paths.
    if sub_id in ['103']:
        lesion_mask_orig = os.path.join(subject_data_dir, '{}_lesion_new.nii.gz'.format(sub_id))
    elif sub_id in ['108']:
        lesion_mask_orig = os.path.join(subject_data_dir, '{}_lesion_new3.nii.gz'.format(sub_id))
    elif sub_id in ['151']:
        lesion_mask_orig = os.path.join(subject_data_dir, '{}_Lesion2.nii.gz'.format(sub_id))
    elif sub_id in ['152','153','154','155']:
        lesion_mask_orig = os.path.join(subject_data_dir, '{}_lesion2.nii.gz'.format(sub_id))
    elif sub_id in ['156']:
        lesion_mask_orig = os.path.join(subject_data_dir, 'Lesion_{}_NEWcg2.nii.gz'.format(sub_id))
    elif sub_id in ['157','160','161','164','165']:
        lesion_mask_orig = os.path.join(subject_data_dir, 'lesion_{}_NEW_cg.nii.gz'.format(sub_id))
    else:
        lesion_mask_orig = os.path.join(subject_data_dir, 'lesion_{}.nii.gz'.format(sub_id))   

    # Check all input paths are valid.
    for in_file in [subject_data_dir, t1_cut_orig, t1_cut_coreg_orig, xfm_orig, lesion_mask_orig]:
        assert os.path.exists(in_file),'{} does not exist!'.format(in_file)
    
    # Create the output directory
    subject_working_dir = os.path.join(WORKING_DIR, sub_id)
    if os.path.exists(subject_working_dir) is False:
        os.mkdir(subject_working_dir)

    # Copy input files to working directory and define paths.
    t1_cut_copy = os.path.join(subject_working_dir, '{}-T1-Cut.nii.gz'.format(sub_id))
    shutil.copy(t1_cut_orig, t1_cut_copy)
    t1_cut_coreg_copy = os.path.join(subject_working_dir, '{}-T1-Cut-CoReg.nii.gz'.format(sub_id))
    shutil.copy(t1_cut_coreg_orig, t1_cut_coreg_copy)
    xfm_copy = os.path.join(subject_working_dir, '{}-T1-Cut.nii_al_mat.aff12.1D.gz'.format(sub_id))
    shutil.copy(xfm_orig, xfm_copy)
    lesion_mask_copy = os.path.join(subject_working_dir, 'lesion_{}.nii.gz'.format(sub_id))
    shutil.copy(lesion_mask_orig, lesion_mask_copy)

    # Define output paths. 
    inverse_xfm = os.path.join(subject_working_dir, '{}_inverse_xfm.aff12.1D'.format(sub_id))
    t1_cut_dereg = os.path.join(subject_working_dir, '{}_t1_cut_dereg.nii.gz'.format(sub_id))
    t1_cut_dereg_padded = os.path.join(subject_working_dir, '{}_t1_cut_dereg_padded.nii.gz'.format(sub_id))
    lesion_mask_bin = os.path.join(subject_working_dir, '{}_lesion_mask_bin.nii.gz'.format(sub_id))
    lesion_mask_bin_dereg = os.path.join(subject_working_dir, '{}_lesion_mask_bin_dereg.nii.gz'.format(sub_id))
    lesion_mask_bin_dereg_padded = os.path.join(subject_working_dir,
            '{}_lesion_mask_bin_dereg_padded.nii.gz'.format(sub_id))
    lesion_mask_bin_dereg_padded_AIL = os.path.join(subject_working_dir,
            '{}_lesion_mask_bin_dereg_padded_AIL.nii.gz'.format(sub_id))

    # Unzip the transform and set the path.
    print(xfm_copy)
    subprocess.check_call(['gunzip {}'.format(xfm_copy)], shell=True)
    xfm = xfm_copy.strip('.gz')
    
    # Get the inverse transform, de-register, and pad the T1 image.
    cat_matvec_cmd = 'cat_matvec -ONELINE {0} -I > {1}'.format(xfm, inverse_xfm)
    subprocess.Popen([cat_matvec_cmd], shell=True)
    subprocess.check_call(['3dAllineate', '-cubic', '-1Dmatrix_apply', inverse_xfm, '-master',
        t1_cut_copy, '-prefix', t1_cut_dereg, t1_cut_coreg_copy])
    subprocess.check_call(['3dZeropad', '-I', '80', '-S', '15', '-prefix', t1_cut_dereg_padded, t1_cut_dereg])
    
    # Binarize, de-register, and pad the lesion mask.
    subprocess.check_call(['fslmaths', lesion_mask_copy, '-bin', lesion_mask_bin])
    subprocess.check_call(['3dAllineate', '-1Dmatrix_apply', inverse_xfm, '-source', lesion_mask_bin,
        '-master', t1_cut_copy, '-prefix', lesion_mask_bin_dereg, '-final', 'NN'])
    subprocess.check_call(['3dZeropad', '-I', '80', '-S', '15', '-prefix',
        lesion_mask_bin_dereg_padded, lesion_mask_bin_dereg])
    subprocess.check_call(['3dresample', '-orient', 'AIL', '-prefix', lesion_mask_bin_dereg_padded_AIL,
        '-inset', lesion_mask_bin_dereg_padded])
