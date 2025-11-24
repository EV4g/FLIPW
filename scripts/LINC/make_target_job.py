import os,sys
import glob
import argparse

def job_template(jobsubname,numcores,timestring,executionstr,basedir):

        jobsub = open(jobsubname,'w')
        jobsub.write('#!/bin/bash\n')
        jobsub.write('#SBATCH -N 1\n')
        jobsub.write('#SBATCH -c %s\n'%numcores)
        jobsub.write('#SBATCH -t %s\n'%timestring)
        jobsub.write('export SINGULARITY_CACHEDIR=%s/../\n'%basedir)
        jobsub.write('export SINGULARITY_PULLDIR=${SINGULARITY_CACHEDIR}\n')
        jobsub.write('export CWL_SINGULARITY_CACHE=${SINGULARITY_PULLDIR}\n')
        jobsub.write('export SINGULARITY_TMPDIR=${SINGULARITY_PULLDIR}\n')

        jobsub.write('ulimit -S -n 35000\n')

        jobsub.write(executionstr)

        return

def make_json_target(msfiles,calsols,outjsonfile):
    msfiles.sort()
    outfile = open(outjsonfile,'w')
    outfile.write('{\n')
    outfile.write('"msin": [ \n')
    for msfile in msfiles:
        outfile.write('{"class":"Directory","path":"%s"},\n'%msfile)
    outfile.write('],\n')
    outfile.write('"selfcal":true,\n')          #selfcal enabled
    outfile.write('"selfcal_strategy":HBA,\n')  #selfcal enabled
    outfile.write('"cal_solutions": {"class":"File","path": "%s"},\n'%calsols)
    outfile.write('}\n')

parser = argparse.ArgumentParser(description='Setting up the target LINC run')
parser.add_argument('--id',type=str,help='ID for run',default="L2014919")
parser.add_argument('--basedir',type=str,help='Directory to start run',default='/project/lspc/Software/shimwell/LINC/run-target')
parser.add_argument('--calsols',type=str,help='Calibrator solutions',default='/project/lspc/Software/shimwell/LINC/run-target/outdir/L2014919/cal_solutions.h5')
args = parser.parse_args()

tarid = args.id
basedir = args.basedir
calsols = args.calsols

# Make the json for running LINC 
msfiles = glob.glob('/project/lspc/Data/floris/P282_full/%s/*.MS'%tarid)
msfiles.sort()
make_json_target(msfiles,calsols,'%s/json-files/%s-tar.json'%(basedir,tarid))

# Make the submit sciprt

executionstr = 'singularity exec -B  /project/lspc/Data/floris/ /project/lspc/Data/floris/linc_latest.sif cwltool --parallel --preserve-entire-environment --no-container  --outdir=%s/outdir/%s/ --log-dir=%s/logs/%s/ /project/lspc/Data/floris/LINC/workflows/HBA_target.cwl %s/json-files/%s-tar.json'%(basedir,tarid,basedir,tarid,basedir,tarid)
print('Submitting target %s job'%tarid)
job_template('%s/submit-scripts/%s_tarjob.sh'%(basedir,tarid),24,'40:00:00',executionstr,basedir)
print('######### Submit job with: sbatch %s/submit-scripts/%s_tarjob.sh'%(basedir,tarid))
print('Outputs will go to:')
print('logs - %s/logs/%s'%(basedir,tarid))
os.system('mkdir %s/logs/%s'%(basedir,tarid))
print('outfiles - %s/outdir/%s'%(basedir,tarid))
os.system('mkdir %s/outdir/%s'%(basedir,tarid))

