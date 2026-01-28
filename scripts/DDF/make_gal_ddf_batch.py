import os
import argparse

def write_slurm_script(filename, observation, linc_dir, output_name, mslist, mask):
    script_content = f"""#!/bin/bash
#SBATCH --job-name={output_name}
#SBATCH --output={output_name}_%j.out
#SBATCH --error={output_name}_%j.err
#SBATCH -N 1
#SBATCH -c 60
#SBATCH -t 120:00:00

# Move to the data/working directory
cd /project/lspc/Data/floris/run-ddf/{observation}

export SINGULARITYENV_RCLONE_CONFIG_DIR=/project/lspc/Data/floris/run-ddf/

# Run the DDF pipeline with Singularity
singularity exec \\
    -B /project/lspc/Data/floris/run-ddf/{observation} \\
    -H /project/lspc/Data/floris/run-ddf/{observation} \\
    /project/lspc/Data/floris/run-ddf/ddf.sif \\
    DDF.py --Misc-IgnoreDeprecationMarking=1 \\
    --Misc-ConserveMemory=1 \\
    --Output-Name={output_name} \\
    --Data-MS={mslist} \\
    --Deconv-PeakFactor 0.010000 \\
    --Data-ColName DATA \\
    --Parallel-NCPU=60 \\
    --Beam-CenterNorm=1 \\
    --Deconv-CycleFactor=0 \\
    --Deconv-MaxMinorIter=1000000 \\
    --Deconv-MaxMajorIter=4 \\
    --Deconv-Mode SSD2 \\
    --Beam-Model=LOFAR \\
    --Weight-Robust -0.50000 \\
    --Image-NPix=20000 \\
    --CF-wmax 50000 \\
    --CF-Nw 100 \\
    --Output-Also onNeds \\
    --Image-Cell 1.500000 \\
    --Facets-NFacets=11 \\
    --SSDClean-NEnlargeData 0 \\
    --Freq-NDegridBand 1 \\
    --Beam-NBand 1 \\
    --Facets-DiamMax 1.5 \\
    --Facets-DiamMin 0.1 \\
    --Deconv-RMSFactor=3.000000 \\
    --SSDClean-ConvFFTSwitch 10000 \\
    --Data-Sort 1 \\
    --Cache-Dir=. \\
    --Cache-DirWisdomFFTW=. \\
    --Debug-Pdb=never \\
    --Log-Memory 1 \\
    --GAClean-RMSFactorInitHMP 1.000000 \\
    --GAClean-MaxMinorIterInitHMP 10000.000000 \\
    --DDESolutions-SolsDir=SOLSDIR \\
    --Cache-Weight=reset \\
    --Beam-LOFARBeamMode=A \\
    --Misc-IgnoreDeprecationMarking=1 \\
    --Beam-At=facet \\
    --Output-Mode=Clean \\
    --Output-RestoringBeam 12.000000 \\
    --Weight-ColName="None" \\
    --Freq-NBand=2 \\
    --RIME-DecorrMode=FT \\
    --SSDClean-SSDSolvePars [S,Alpha] \\
    --SSDClean-BICFactor 0 \\
    --Mask-Auto=1 \\
    --Mask-SigTh=5.00 \\
    --Mask-External={mask} \\
    --Selection-UVRangeKm=[0.100000,1000.000000] \\
    --GAClean-MinSizeInit=10
"""
    with open(filename, "w") as file:
        file.write(script_content)

parser = argparse.ArgumentParser(description='Setting up the DDF pipeline SLURM batch')
parser.add_argument('--observation', type=str, help='observation-ID for run', required=True)
parser.add_argument('--linc_dir', type=str, help='linc_out or linc_out_uncompressed', default='linc_out')
parser.add_argument('--output_name', type=str, help='output name for DDF run', default='SSD2')
parser.add_argument('--mslist', type=str, help='path to mslist.txt', default='mslist.txt')
parser.add_argument('--mask', type=str, help='path to mask file', default='external_mask.fits')

args = parser.parse_args()

filename = f"{args.output_name}_submit.sh"
write_slurm_script(os.path.join(args.observation, filename), args.observation, args.linc_dir, args.output_name, args.mslist, args.mask)

