#!/bin/bash
#SBATCH --job-name=add_hogbom
#SBATCH --output=add_hogbom_to_data_%j.out
#SBATCH --error=add_hogbom_to_data_%j.err
#SBATCH -N 1
#SBATCH -c 60
#SBATCH -t 2:00:00
#SBATCH -p infinite

# Move to the data/working directory
cd /project/lspc/Data/floris/run-ddf/SSD2_predict_2

export SINGULARITYENV_RCLONE_CONFIG_DIR=/project/lspc/Data/floris/run-ddf/

# Run the DDF pipeline with Singularity
singularity exec \
    -B /project/lspc/Data/floris/run-ddf/imaging_tests/SSD2_predict_2 \
    -H /project/lspc/Data/floris/run-ddf/imaging_tests/SSD2_predict_2 \
    /project/lspc/Data/floris/run-ddf/ddf.sif \
    DDF.py --Output-Name=Hogbom3_predict \
    --Data-MS=big-mslist.txt \
    --Data-ColName=DATA \
    --Output-Mode=Predict \
    --Predict-InitDicoModel=Hogbom3.DicoModel \
    --Predict-ColName=MODEL_DATA \
    --Deconv-Mode=Hogbom \
    --Image-Cell=1.5 \
    --Image-NPix=20000 \
    --Beam-Model=LOFAR \
    --Beam-LOFARBeamMode=A \
    --Beam-CenterNorm=1 \
    --Beam-At=facet \
    --Facets-NFacets=11 \
    --Freq-NBand=2 \
    --Freq-NDegridBand=1 \
    --CF-wmax=50000 \
    --CF-Nw=150 \
    --Parallel-NCPU=60