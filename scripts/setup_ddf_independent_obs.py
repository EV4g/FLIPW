#pseudocode
#locate .sif file
#locate tier1-config.cfg file
#locate linc_out folder
#   locate linc_out subfolders L* --> one per observation
#   check if it has linc_out or linc_out_uncompressed
#locate catalogue folder

#setup folders per observation
#   each should at the end contain
#   [L-observation]
#       tier1-config.cfg
#       mslist.txt
#       bigmslist.txt
#       linc_out(_uncompressed)/
#           L-observation/
#               results/
#                   *.ms
#

#optional locate linc_out_uncompressed
#   if not found --> optional DP3 runner before copying [metadata_uncompressor.py]

#generate sbatch file [make_ddf_batch.py]


import os
import glob
import subprocess

decompress = False #enable if LINC compressed the data, but you're using a ddf version that cannot handle that yet.

#### setup
try:
    singularity_image = glob.glob("flocs*.sif")[0] #"flocs_v6.0.0_znver2_znver2.sif"
    print("Using", singularity_image)
except:
    print("No .sif file found")

try:
    config_file = glob.glob("*.cfg")[0] #"tier1-config.cfg"
    print("Using", config_file)
except:
    print("No .cfg file found")

# check linc-target dir
linc_dir = glob.glob("linc_out*")[0]
print("Using", linc_dir)

observations = [folder.split("/")[-1] for folder in glob.glob(linc_dir + "/*")]
print("Found observations:", observations)

# make dirs for each obs
for obs in observations:
    os.makedirs(obs, exist_ok=True)
    print("Made dir:", obs)

#### check compression requirements
if (linc_dir == "linc_out") and (decompress == True):
    try:    
        glob.glob("metadata_uncompressor.py")[0]
        print("Decompression started")
        subprocess.run("python3", "metadata_uncompressor.py")
        print("Decompression done")
    except:
	print("Decompressor not found, skipping")

    # make linc_out_uncompressed
    # uncompress the *.ms files with DP3
else:
    print("Decompression step skipped, not needed")
