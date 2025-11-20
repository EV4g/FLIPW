import os
import glob
from pathlib import Path
import subprocess

filelocation = "linc_out/L*/results/*ms"
outdir = "linc_out_uncompressed/"

filelist = glob.glob(filelocation)

for i, msfile in enumerate(filelist):
    observation = Path(msfile).parts[1]
    filename = Path(msfile).parts[-1]

    print("["+str(i + 1)+" / "+str(len(filelist))+"]", filename)

    outlocation = os.path.join(outdir, observation, "results")
    os.makedirs(outlocation, exist_ok=True)
    outfile = os.path.join(outlocation, filename)

    command = f"DP3 msin={msfile} msout={outfile} steps=[] msout.scalarflags=False  msout.uvwcompression=False msout.antennacompression=False"
    subprocess.run(command, shell=True, check=True, executable="/bin/bash")
