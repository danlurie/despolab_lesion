# Notes from testing to de-register masks drawn by Emi/Caterina 
# 
# At the time of testing, input files lived in:
# ../rstate/data/Rest.Lesion/Data/*/Rest

# De-register the anatomical image (for testing purposes)
cat_matvec -ONELINE 123-T1-Cut.nii_al_mat.aff12.1D -I > 123-T1-Cut.nii_al_mat_inverse.aff12.1D

3dAllineate -cubic -1Dmatrix_apply 123-T1-Cut.nii_al_mat_inverse.aff12.1D -master 123-T1-Cut.nii.gz -prefix 123-T1-Cut-DeReg.nii.gz 123-T1-Cut-CoReg.nii.gz

3dZeropad -I 80 -S 15 -prefix 123-T1-Cut-DeReg-Padded.nii.gz 123-T1-Cut-DeReg.nii.gz

# De-register the lesion mask (which we can compare to the de-registered anatomical)
fslmaths lesion_123.nii.gz -bin lesion_123_bin.nii.gz 

3dAllineate -1Dmatrix_apply 123-T1-Cut.nii_al_mat_inverse.aff12.1D -source lesion_123_bin.nii.gz -master 123-T1-Cut.nii.gz -prefix lesion_123_bin_DeReg.nii.gz -final NN

3dZeropad -I 80 -S 15 -prefix lesion_123_bin_DeReg_Padded.nii.gz lesion_123_bin_DeReg.nii.gz

3dresample -orient AIL -prefix lesion_123_bin_DeReg_Padded_AIL.nii.gz -inset lesion_123_bin_DeReg_Padded.nii.gz
