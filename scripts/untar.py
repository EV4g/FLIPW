#Script to untar data retrieved from the LTA by using wget
#SRMFifoGet.py?surl=srm:%2F%2Fsrm.grid.sara.nl:8443%2Fpnfs%2Fgrid.sara.nl%2Fdata%2Flofar%2Fops%2Fprojects%2Flofarschool%2F246403%2FL246403_SAP000_SB000_uv.MS_7d4aa18f.tar
#This scripts will rename those files as the string after the last '%'

import os
import glob
import argparse

parser = argparse.ArgumentParser(description='Untar LTA files')
parser.add_argument('--dir', type=str, help='Directory with .tar files')
args = parser.parse_args() 
dir_with_tars = args.dir

path = os.path.join(os.getcwd(), dir_with_tars)
os.chdir(path)
print("path:", path)

filelist = glob.glob(path + "*SB*.tar*") 
nr = len(filelist)
print("Amount of files to untar:", nr)

if nr > 0:
    for i, filename in enumerate(filelist):
        outname = filename.split("%")[-1]
        observation = outname.split("_")[0]

        obs_dir = os.path.join(path, observation)
        os.makedirs(obs_dir, exist_ok=True)
        new_tar_path = os.path.join(obs_dir, outname)


        os.rename(filename, new_tar_path)
        os.system(f'tar -xf {new_tar_path} -C {obs_dir}')
        os.system(f'rm -r {new_tar_path}')

        print("["+str(i + 1)+" / "+str(nr)+"]", "file:", outname+' untarred.')
