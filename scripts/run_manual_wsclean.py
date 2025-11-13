import os
import argparse

def create_wsclean_slurm_script(name, observation, ms_file_location):
    outfile = f"run_{name}_{observation}_wsclean.sh"
    working_dir = "/project/lspc/Data/floris/"
    sif_file = working_dir+"linc_latest.sif"

    # all files in ms_file_location
    ms_files = sorted([os.path.join(ms_file_location, f) for f in os.listdir(ms_file_location)])
    if len(ms_files) == 0:
        print("Error: No .ms files found in target dir.")
        return
    else:
        print(len(ms_files), "files located")

    ms_files_lines = " \\\n    ".join(ms_files)
    output_dir = f"/project/lspc/Data/floris/manual_wcs/{name}/{observation}/"

    # wsclean
    wsclean_cmd = (
        "wsclean \\\n"
        "    -j 24 \\\n"
        "    -auto-mask 3 \\\n"
        "    -auto-threshold 0.3 \\\n"
#       "    -auto-threshold 5 \\\n"
        "    -channels-out 7 \\\n"
        "    -deconvolution-channels 3 \\\n"
        "    -fit-spectral-pol 3 \\\n"
        f"    -name {observation} \\\n"
        "    -scale 15asec \\\n"
        "    -size 2500 2500 \\\n"
        "    -join-channels \\\n"
        "    -maxuvw-m 20000 \\\n"
        "    -mgain 0.8 \\\n"
        "    -multiscale \\\n"
        "    -niter 10000 \\\n"
        "    -nmiter 5 \\\n"
        "    -no-update-model-required \\\n"
        "    -parallel-deconvolution 1500 \\\n"
        "    -parallel-reordering 4 \\\n"
        "    -save-source-list \\\n"
        "    -taper-gaussian 40asec \\\n"
        "    -temp-dir /tmp \\\n"
        "    -use-wgridder \\\n"
        "    -weight briggs -0.5 \\\n"
        f"    {ms_files_lines}"
    )

    # SLURM script content
    script = f"""#!/bin/bash
#SBATCH --job-name=wsc_{observation}
#SBATCH --output={observation}_wsclean.out
#####SBATCH --error={observation}_wsclean.err
#SBATCH -N 1
#SBATCH -c 24
#SBATCH -t 8:00:00

mkdir -p {output_dir}

cd {output_dir}

echo "Running manual wsclean for {observation}. Outdir is {output_dir}"

singularity exec --bind {working_dir} {sif_file} bash -c '{wsclean_cmd}'
"""

    with open(outfile, 'w') as f:
        f.write(script)
    print(f"SLURM script written to {outfile}")



#variables
parser = argparse.ArgumentParser(description="Setup SLURM script for manual wsclean run")
parser.add_argument('--observation', type=str, default='L2020624', help='Observation ID (default: L2020624)')
args = parser.parse_args()

name = "P282+00"
observation = args.observation
ms_file_location = f"/project/lspc/Data/floris/run-target/outdir/{observation}/results/"

#create the .sh file
create_wsclean_slurm_script(name, observation, ms_file_location)
