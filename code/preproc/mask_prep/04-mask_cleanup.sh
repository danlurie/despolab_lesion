# This script "cleans up" lesion masks by filling holes and smothing edges.

cd /home/despoB/lesion/mask_prep/clean/;

for mask in `ls /home/despoB/lesion/mask_prep/combined/`; do
    pid=$(echo $mask | cut -c 1-3)
    c3d /home/despoB/lesion/mask_prep/combined/${pid}_manual_mask.nii.gz \
        -binarize -o tmp_${pid}_bin.nii.gz;
    ImageMath 3 tmp_${pid}_bin_MC.nii.gz MC tmp_${pid}_bin.nii.gz 1;
    c3d tmp_${pid}_bin_MC.nii.gz -binarize -o tmp_${pid}_bin_MC_bin.nii.gz;
    ImageMath 3 tmp_${pid}_bin_MC_bin_ME.nii.gz ME tmp_${pid}_bin_MC_bin.nii.gz 1;
    c3d tmp_${pid}_bin_MC_bin_ME.nii.gz -binarize -o ${pid}_clean_mask.nii.gz;
    echo "Mask cleanup completed for patient $pid" 
done
