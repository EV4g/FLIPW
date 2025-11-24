import os
import glob
from pathlib import Path
import subprocess
from termcolor import colored

filelocation = "linc_out/L*/results/*ms"
outdir = "linc_out_uncompressed/"

filelist = glob.glob(filelocation)

for i, msfile in enumerate(filelist):
    observation = Path(msfile).parts[1]
    filename = Path(msfile).parts[-1]

    print(colored("["+str(i + 1)+" / "+str(len(filelist))+"]  "+str(filename), "green"))

    outlocation = os.path.join(outdir, observation, "results")
    os.makedirs(outlocation, exist_ok=True)
    outfile = os.path.join(outlocation, filename)

    command = f"DP3 msin={msfile} msout={outfile} steps=[] msout.scalarflags=False  msout.uvwcompression=False msout.antennacompression=False"
    subprocess.run(command, shell=True, check=True, executable="/bin/bash")
