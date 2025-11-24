
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

def make_json_calibrator(msfiles,outjsonfile):
    msfiles.sort()
    outfile = open(outjsonfile,'w')
    outfile.write('{\n')
    outfile.write('"msin": [ \n')
    for msfile in msfiles:
        outfile.write('{"class":"Directory","path":"%s"},\n'%msfile)
    outfile.write('],\n')
    outfile.write('"refant": "CS00.*"\n')
    #outfile.write('"flag_baselines": [],\n')
    #outfile.write('"process_baselines_cal": "*&",\n')
    #outfile.write('"filter_baselines": "*&",\n')
    #outfile.write('"fit_offset_PA": false,\n')
    #outfile.write('"do_smooth": false,\n')
    #outfile.write('"rfi_strategy": "$LINC_DATA_ROOT/rfistrategies/lofar-default.lua",\n')
    #outfile.write('"max2interpolate": 30,\n')
    #outfile.write('"ampRange": [0,0],\n')
    #outfile.write('"skip_international": true,\n')
    #outfile.write('"raw_data": false,\n')
    #outfile.write('"propagatesolutions": true,\n')
    #outfile.write('"flagunconverged": false,\n')
    #outfile.write('"maxStddev": -1.0,\n')
    #outfile.write('"solutions2transfer": null,\n')
    #outfile.write('"antennas2transfer": "[FUSPID].*",\n')
    #outfile.write('"do_transfer": false,\n')
    #outfile.write('"trusted_sources": "3C48,3C147,3C196,3C295,3C380",\n')
    #outfile.write('"demix_sources": ["VirA_4_patch", "CygAGG", "CasA_4_patch", "TauAGG"],\n')
    #outfile.write('"demix_freqres": "48.82kHz",\n')
    #outfile.write('"demix_timeres": 10,\n')
    #outfile.write('"demix": false,\n')
    #outfile.write('"ion_3rd": false,\n')
    #outfile.write('"clock_smooth": true,\n')
    #outfile.write('"tables2export": "clock",\n')
    #outfile.write('"max_dppp_threads": 24\n')
    #outfile.write('"memoryperc": 20,\n')
    #outfile.write('"min_length": 50,\n')
    #outfile.write('"overhead": 0.8,\n')
    #outfile.write('"min_separation": 30,\n')
    #outfile.write('"max_separation_arcmin": 1.0,\n')
    #outfile.write('"calibrator_path_skymodel": null,\n')
    #outfile.write('"A-Team_skymodel": null,\n')
    #outfile.write('"avg_timeresolution": 4,\n')
    #outfile.write('"avg_freqresolution": "48.82kHz",\n')
    #outfile.write('"bandpass_freqresolution": "195.3125kHz",\n')
    #outfile.write('"lbfgs_historysize" : 10,\n')
    #outfile.write('"lbfgs_robustdof" : 200\n')
    outfile.write('}\n')

parser = argparse.ArgumentParser(description='Setting up the calibrator LINC run')
parser.add_argument('--id',type=str,help='ID for run',default="L2014919")
parser.add_argument('--basedir',type=str,help='Directory to start run',default='/project/lspc/Software/shimwell/LINC/run-calibrator')
args = parser.parse_args()

calid = args.id
basedir = args.basedir

# Make the json for running LINC 
msfiles = glob.glob('/project/lspc/Data/floris/P282_full/%s/*.MS'%calid)
msfiles.sort()
make_json_calibrator(msfiles,'%s/json-files/%s-cal.json'%(basedir,calid))

# Make the submit sciprt

executionstr = 'singularity exec -B  /project/lspc/Data/floris/ /project/lspc/Data/floris/linc_latest.sif cwltool --parallel --preserve-entire-environment --no-container  --outdir=%s/outdir/%s/ --log-dir=%s/logs/%s/ /project/lspc/Data/floris/LINC/workflows/HBA_calibrator.cwl %s/json-files/%s-cal.json'%(basedir,calid,basedir,calid,basedir,calid)
print('Submitting calibrator %s job'%calid)
job_template('%s/submit-scripts/%s_caljob.sh'%(basedir,calid),24,'40:00:00',executionstr,basedir)
print('######### Submit job with: sbatch %s/submit-scripts/%s_caljob.sh'%(basedir,calid))
print('Outputs will go to:')
print('logs - %s/logs/%s'%(basedir,calid))
os.system('mkdir %s/logs/%s'%(basedir,calid))
print('outfiles - %s/outdir/%s'%(basedir,calid))
os.system('mkdir %s/outdir/%s'%(basedir,calid))

