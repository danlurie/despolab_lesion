import subprocess
import os
import sys

sub_id = sys.argv[1]

DATA_DIR = '/home/despoB/lesion/data/original/nifti'
MASK_DIR = '/home/despoB/lesion/mask_prep/combined'
OUT_DIR = '/home/despo/dlurie/Projects/despolab_lesion/anat_preproc/testing'

BRAIN_EXTRACTION_T1_TEMPLATE = '/home/despo/dlurie/Projects/despolab_lesion/anat_preproc/templates/adni/adni_2mm_t1_template.nii.gz'
BRAIN_EXTRACTION_PROBABILITY_MASK_TEMPLATE = '/home/despo/dlurie/Projects/despolab_lesion/anat_preproc/templates/adni/adni_2mm_brain_prob_mask.nii.gz'
REGISTRATION_T1_TEMPLATE = '/home/despo/dlurie/Projects/despolab_lesion/anat_preproc/templates/MNI/mni_2mm.nii.gz'

# Get the path to the patient data directory.
sub_data_dir = os.path.join(DATA_DIR, 'sub_{}'.format(sub_id))
# Only continue of the patient input directory actually exists.
if not os.path.isdir(sub_data_dir):
    raise OSError('No input data exists for patient {}.'.format(sub_id))
# Get the path to the patient output directory.
sub_out_dir = os.path.join(OUT_DIR, sub_id)
# Create the patient output directory if it doesn't exist.
if not os.path.isdir(sub_out_dir):
    os.mkdir(sub_out_dir)

# Set input and output paths for mask transformations.
multi_class_lesion_mask = os.path.join(MASK_DIR, '{}_manual_mask.nii.gz'.format(sub_id))
# Only continue of the patient mask exists.
if not os.path.exists(multi_class_lesion_mask):
    raise OSError('No mask exists for patient {}.'.format(sub_id))

# Define output paths for mask transformations.
binary_lesion_mask = os.path.join(sub_out_dir, 'binary_lesion_mask.nii.gz')
lesion_mask_dilated = os.path.join(sub_out_dir, 'lesion_mask_dilated.nii')
inverse_lesion_mask = os.path.join(sub_out_dir, 'inverse_lesion_mask.nii')


# Run mask transformations
print("Binarizing multi-class lesion mask...")
subprocess.check_call(['fslmaths', multi_class_lesion_mask, '-bin', binary_lesion_mask])
print("Dilating binary lesion mask...")
subprocess.check_call(['ImageMath', '3', lesion_mask_dilated, 'MD', binary_lesion_mask, '2'])
print("Creating inverse lesion mask...")
subprocess.check_call(['ImageMath', '3', inverse_lesion_mask, 'Neg', lesion_mask_dilated])

# Set which mask to use during registration.
patient_registration_mask = lesion_mask_dilated
# Set the path to the patient T1 image.
patient_t1_orig = os.path.join(sub_data_dir, 'anat', 't1mprage.nii.gz')
# Set the output directory and path prefix for brain extraction.
brain_extraction_out_dir = os.path.join(sub_out_dir, 'ants_brain_extraction_w_reg_mask')
brain_extraction_out_prefix = os.path.join(brain_extraction_out_dir, '{}_'.format(sub_id))
print("Running brain extraction...")
subprocess.check_call(['antsBrainExtraction.sh',
                        '-d', '3',
                        '-a', patient_t1_orig,
                        '-e', BRAIN_EXTRACTION_T1_TEMPLATE,
                        '-m', BRAIN_EXTRACTION_PROBABILITY_MASK_TEMPLATE,
                        '-f', patient_registration_mask,
                        '-k', '1',
                        '-o', brain_extraction_out_prefix])
# Set the path to the brain mask.
brain_mask = os.path.join(brain_extraction_out_dir, '{}_BrainExtractionMask.nii.gz'.format(sub_id))
# Set the output directory and path prefix for tissue segmentation.
tissue_segmentation_out_dir = os.path.join(sub_out_dir, 'ants_tissue_segmentation')
tissue_segmentation_out_prefix = os.path.join(tissue_segmentation_out_dir, '{}_'.format(sub_id))
print("Running tissue segmentation...")
subprocess.check_call(['antsAtroposN4.sh',
                        '-d', '3',
                        '-a', patient_t1_orig,
                        '-x', brain_mask,
                        '-c', '3',
                        '-k', '1',
                        '-o', tissue_segmentation_out_prefix])
# Set the path to the bias-field corrected T1 image.
patient_t1_n4_corrected = os.path.join(tissue_segmentation_out_dir, '{}_Segmentation0N4.nii.gz'.format(sub_id))
# Set the output directory and path prefix for registration.
## SOMETHING GOES WRONG HERE? Trouble creating the output directory or files?
## 'Can't write <file>...' error
registration_out_dir = os.path.join(sub_out_dir, 'ants_registration_w_reg_mask')
registration_out_prefix = os.path.join(registration_out_dir, '{}_'.format(sub_id))
print("Running registration...")
subprocess.check_call(['antsRegistrationSyN.sh',
                        '-d', '3',
                        '-f', patient_t1_n4_corrected,
                        '-m', REGISTRATION_T1_TEMPLATE,
                        '-x', patient_registration_mask,
                        '-o', registration_out_prefix])


