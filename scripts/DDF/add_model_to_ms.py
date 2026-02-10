import os
import glob
import argparse

def write_slurm_script(filename, dir, modelname, modeltype, linc_dir):
    script_content = f"""#!/bin/bash
#SBATCH --job-name={filename}
#SBATCH --output={filename}_%j.out
#SBATCH -N 1
#SBATCH -c 60
#SBATCH -t 5:00:00
#SBATCH -p infinite

cd {dir}

export SINGULARITYENV_RCLONE_CONFIG_DIR=/project/lspc/Data/floris/run-ddf/

# Run the DDF pipeline with Singularity
singularity exec \\
    -B {dir} \\
    -H {dir} \\
    /project/lspc/Data/floris/run-ddf/ddf.sif \\
    DDF.py --Output-Name={modelname} \\
    --Data-MS=big-mslist.txt \\
    --Data-ColName=DATA \\
    --Output-Mode=Predict \\
    --Predict-InitDicoModel={modelname} \\
    --Predict-ColName=MODEL_DATA \\
    --Deconv-Mode={modeltype} \\
    --Image-Cell=1.5 \\
    --Image-NPix=20000 \\
    --Beam-Model=LOFAR \\
    --Beam-LOFARBeamMode=A \\
    --Beam-CenterNorm=1 \\
    --Beam-At=facet \\
    --Facets-NFacets=11 \\
    --Freq-NBand=2 \\
    --Freq-NDegridBand=1 \\
    --CF-wmax=50000 \\
    --CF-Nw=100 \\
    --Parallel-NCPU=60 \\
"""
    with open(filename, "w") as file:
        file.write(script_content)

parser = argparse.ArgumentParser(description='Setting up the ddf run')
parser.add_argument('--modelname', type=str, help='Name of DicoModel file', required=True)
parser.add_argument('--modeltype', type=str, help='Type of model [Hogbom, SSD2, ...]', required=True)
parser.add_argument("--linc_dir", type=str, help='linc directory', required=True)
args = parser.parse_args()

filename = args.modelname+"_merge_submit.sh"
basedir = os.getcwd()

write_slurm_script(filename, args.dir, args.modelname, args.modeltype, args.lincdir)

print(f"Succesfully written to file {filename}")