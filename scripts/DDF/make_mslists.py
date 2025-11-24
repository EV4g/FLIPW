#!/usr/bin/env python
# Make MS lists, checking for heavily flagged data

from __future__ import print_function
import os
import glob
import pyrap.tables as pt
import numpy as np
import argparse

def check_flagged(ms):
    t = pt.table(ms, readonly=True)
    tc = t.getcol('FLAG').flatten()
    return float(np.sum(tc))/len(tc)

def check_flags_and_shape(ms):
    t = pt.table(ms, readonly=True)
    flags = t.getcol('FLAG')
    channels=flags.shape[1]
    tc = flags.flatten()
    return channels,float(np.sum(tc))/len(tc)

def get_timerange(ms):
    t = pt.table(ms +'/OBSERVATION', readonly=True, ack=False)
    return t.getcell('TIME_RANGE',0)

def make_list(workdir='.',force=False):
    g=sorted(glob.glob(workdir))
    full_mslist=[]
    start_times=[]
    chanlist=[]
    for i, ms in enumerate(g):
        chans,ff=check_flags_and_shape(ms)
        t0,t1=get_timerange(ms)
        print("["+str(i+1)+" / "+str(len(g))+ "]", ms.split("/")[-1], chans, ff)
        if ff<0.8 and (len(chanlist)==0 or chans in chanlist):
            full_mslist.append(os.path.basename(ms))
            start_times.append(t0)
            chanlist.append(chans)
    full_mslist = np.array(full_mslist)

    # check for multiple observations
    Ustart_times = np.unique(start_times)

    # ensure lists contain all ms from all observations and same subset for each observation
    write_full_mslist = np.array(())
    write_mslist = np.array(())
    for start_time in Ustart_times:
        write_full_mslist = np.hstack((write_full_mslist,full_mslist[start_times==start_time]))
        write_mslist = np.hstack((write_mslist,full_mslist[start_times==start_time][2::4]))

    open(os.getcwd()+'/big-mslist.txt','w').writelines(ms+'\n' for ms in write_full_mslist)
    open(os.getcwd()+'/mslist.txt','w').writelines(ms+'\n' for ms in write_mslist)
    return


parser = argparse.ArgumentParser(description='making the ms file list')
parser.add_argument('--dir',type=str,help='ms file location', default=os.getcwd())
args = parser.parse_args()
ms_dir = args.dir

print("Looking for files in:", ms_dir)
print("Found", len(glob.glob(ms_dir)), "files in dir")
make_list(workdir=ms_dir)
print("Done")
