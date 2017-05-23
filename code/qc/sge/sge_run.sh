#!/bin/sh
source /home/despoB/dlurie/.bashrc;
source activate mriqc;
SUB_ID="${SGE_TASK}";
cd /home/despoB/dlurie/Projects/despolab_lesion/qc;
mriqc \
    --participant_label $SUB_ID \
    -m T1w bold \
    --n_procs 5 \
    --mem_gb 8 \
    --ica \
    --ants-nthreads 3\
    -w /home/despoB/dlurie/Projects/despolab_lesion/qc/work \
    --verbose-reports \
    /home/despoB/lesion/data/original/bids/ \
    /home/despoB/dlurie/Projects/despolab_lesion/qc/out \
    participant 
END_TIME=$(date);
echo "QC pipeline for patient $SUB_ID completed at $END_TIME";


