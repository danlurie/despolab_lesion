"""
BIC DICOM to NIfTI Conversion Script - Written by Dan Lurie (dan.lurie@berkeley.edu)

Designed for use on data from the UC Berkeley Brain Imaging Center.

Requires dcm2nii (http://www.mccauslandcenter.sc.edu/mricro/mricron/dcm2nii.html).

This script will convert all anatomical (MPRAGE) and functional (EPI) scans for all subjects in a directory.

Usage:
======

python bic_dcm2nii.py DICOM_DIR NIFTI_DIR


Notes:
====== 
   
DICOM_DIR: The path to a directory containing your subject folders.
           Each subject folder should contain the following:
	   - At least one anatomical scan (i.e. a folder with 'T1MPRAGE' somewhere in it's name).
	   - At least one functional scan (i.e. a folder with 'EPI' somewhere in it's name).

NIFTI_DIR: A directory where you would like NIfTI files written.
	   If this directory does not exist, one will be created.
"""

import os
import re
import subprocess

DICOM_DIR = '/home/despoB/lesion/data/original/dicom'
NIFTI_DIR = '/home/despoB/lesion/data/original/nifti'
PROTOCOL = 0

# Check input and output directories.
if not os.path.isdir(DICOM_DIR):
    raise OSError('Invalid path provided for input DICOM directory.')
if not os.path.isdir(NIFTI_DIR):
    raise OSError('Invalid path provided for output NIFTI directory.')
if not os.access(NIFTI_DIR, os.W_OK):
    raise OSError('The output NIFTI directory is write protected.')

# Define scan protocols.
if PROTOCOL == 0:
    # Define regular expressions to match T1, T2, FLAIR and EPI scan names. 
    mprage_rgx = re.compile('(.*t1_mprage.*)', re.IGNORECASE)
    tirm_rgx = re.compile('(.*t2_tirm_tra_darkfluid_[1-3]mm.*)', re.IGNORECASE)
    tse_rgx = re.compile('(.*t2_tse_tra_448_[1-3]mm.*)', re.IGNORECASE)
    t2w_rgx = re.compile('(.*T2W_1mmISO.*)', re.IGNORECASE)
    flair_rgx = re.compile('(.*t2_flair_1x1x1.*|.*T2FLAIR_1mmISO.*)', re.IGNORECASE)
    pcasl_rgx = re.compile('(.*PCASL_1500ms.*)', re.IGNORECASE)
    epi_rgx = re.compile('(.*EPI_Template__physiomatched.*|.*EPITemplatephysiomatched.*)', re.IGNORECASE)

    # Define the list of subjects scanned with this protocol
    subject_list = [189]

# Loop through subjects.
for subject in subject_list:
    # Get the subject DICOM directory.
    subject_DICOM_dir = os.path.join(DICOM_DIR, str(subject))
    # Get a list of sub-directories (hopefully containing DICOMS).
    if os.path.isdir(subject_DICOM_dir):
        subject_subdir_list = os.listdir(subject_DICOM_dir)
    else:
        print("Unable to find DICOM directory for subject {}, skipping to next subject.".format(str(subject)))
        continue
    # Create sub-directories for NIFTI files.
    subject_NIFTI_dir = os.path.join(NIFTI_DIR, "sub_"+str(subject))
    nifti_anat_subdir = os.path.join(subject_NIFTI_dir, 'anat') 
    nifti_func_subdir = os.path.join(subject_NIFTI_dir, 'func')    
    for folder in [subject_NIFTI_dir, nifti_anat_subdir, nifti_func_subdir]:
        if not os.path.isdir(folder):
            os.mkdir(folder)
    # Select only the scans we want to convert.
    if len(subject_subdir_list) >= 1:
        # MPRAGE
        mprage_scans = [m.group(1) for i in subject_subdir_list for m in [mprage_rgx.search(i)] if m]
        mprage_scans = [scan for scan in mprage_scans if "XX" not in scan]
        # TIRM
        tirm_scans = [m.group(1) for i in subject_subdir_list for m in [tirm_rgx.search(i)] if m]
        tirm_scans = [scan for scan in tirm_scans if "XX" not in scan]
        # TSE
        tse_scans = [m.group(1) for i in subject_subdir_list for m in [tse_rgx.search(i)] if m]
        tse_scans = [scan for scan in tse_scans if "XX" not in scan]
        # T2W
        t2w_scans = [m.group(1) for i in subject_subdir_list for m in [t2w_rgx.search(i)] if m]
        t2w_scans = [scan for scan in t2w_scans if "XX" not in scan]
        # FLAIR
        flair_scans = [m.group(1) for i in subject_subdir_list for m in [flair_rgx.search(i)] if m]
        flair_scans = [scan for scan in flair_scans if "XX" not in scan]
        # PCASL
        pcasl_scans = [m.group(1) for i in subject_subdir_list for m in [pcasl_rgx.search(i)] if m]
        pcasl_scans = [scan for scan in pcasl_scans if "XX" not in scan]
        # EPI
        epi_scans = [m.group(1) for i in subject_subdir_list for m in [epi_rgx.search(i)] if m]
        epi_scans = [scan for scan in epi_scans if "XX" not in scan]

    else:
        print("DICOM directory for subject {} is empty, skipping to next stubject.".format(str(subject)))
        continue
    # Exclude subjects where we have found more than one scan of each type. If there
    # are two, it usually means the first is bad.

    # Deal with subjects missing one of the T2 scans.

    # Loop through scans and runs.
    print("Converting scans for subject {}.".format(str(subject)))
    
    # Convert anatomical scans
    for scan in [mprage_scans, tirm_scans, tse_scans, t2w_scans, flair_scans]:
        if len(scan) >= 1:
            for run in scan:
                print("Converting {}.".format(os.path.join(subject_DICOM_dir, run)))
                subprocess.check_call(['dcm2nii', '-o', nifti_anat_subdir, os.path.join(subject_DICOM_dir, run)])
    
    # Convert functional scans
    for scan in [pcasl_scans, epi_scans]:
        if len(scan) >= 1:
            for run in scan:
                print("Converting {}.".format(os.path.join(subject_DICOM_dir, run)))
                subprocess.check_call(['dcm2nii', '-o', nifti_func_subdir, os.path.join(subject_DICOM_dir, run)])
