#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Marine User Guide data merger

This script creates a view of a source-deck data in a Marine User Guide version
by linking the level2 files in the data releases directories to a common
directory in the User Guide directory in the data space.

Input arguments to this script are:
    
    * sd: source-deck id (sss-ddd)
    * data_path: path to the general marine data directory
    * mug_path: path to the data directory of the marine user guide version
    * mug_config_file: path to the Marine User Guide data configuration file
    
"""
import sys
import os
import glob
import json
import logging
from subprocess import call
from imp import reload
reload(logging)  # This is to override potential previous config of logging


# FUNCTIONS -------------------------------------------------------------------
class script_setup:
    def __init__(self, inargs):
        self.data_path = inargs[1]
        self.mug_path = inargs[2]
        self.mug_config_file = inargs[3]
        self.sd = inargs[4]

def split_filename(filename):
    # Remove extension just in case (optional)
    parts = filename.split("-")

    # First part: everything up to the year (before YYYY-MM)
    # Find the year-month segment (should be digits and 4-2 format)
    for i in range(len(parts)):
        if i + 1 < len(parts):
            # Check if part[i] is a 4-digit year and part[i+1] is a 2-digit month
            if parts[i].isdigit() and len(parts[i]) == 4 and parts[i+1].isdigit() and len(parts[i+1]) == 2:
                first = "-".join(parts[:i])
                year_month = f"{parts[i]}-{parts[i+1]}"
                rest = "-".join(parts[i+2:])
                return [first, year_month, rest]
    
    return [filename]         

# MAIN ------------------------------------------------------------------------
def main():
    # Process input and set up some things and make sure we can do something---
    logging.basicConfig(format='%(levelname)s\t[%(asctime)s](%(filename)s)\t%(message)s',
                        level=logging.INFO,datefmt='%Y%m%d %H:%M:%S',filename=None)
    if len(sys.argv)>1:
        logging.info('Reading command line arguments')
        args = sys.argv
    else:
        logging.error('Need arguments to run!')
        sys.exit(1)
    
    params = script_setup(args)
    
    
    with open(params.mug_config_file,'r') as fO:
        mug_config = json.load(fO)
    
    year_end_common = mug_config.get("year_end")
    year_init_common = mug_config.get("year_init")
    
    dataset_dict = mug_config.get("datasets")
    
    sd_path_um = os.path.join(params.mug_path,'level2',params.sd)

    for release in dataset_dict.keys():
        for dataset in dataset_dict[release].keys():
            year_init = dataset_dict[release][dataset].get("year_init")
            year_end = dataset_dict[release][dataset].get("year_end")
            year_init = max(year_init_common, year_init)
            year_end = min(year_end_common, year_end)
            sid_dck_dict = dataset_dict[release][dataset].get("sid_dck")
            if not isinstance(sid_dck_dict, dict):
                logging.info(f"No decks selected for {dataset} {release}.")
                continue
            if params.sd not in sid_dck_dict.keys():
                logging.info(f"{params.sd} not available for {dataset} {release}.")
                continue
            exclude = sid_dck_dict.get("exclude")
            if exclude is True:
                logging.info(f"Exclude {dataset} {release} {params.sd}.")
                continue
            exclude_params = sid_dck_dict.get("params_exclude", [])
            all_files = glob.glob(os.path.join(params.data_path, release, dataset, "level2", params.sd, "*.psv"))
            selected_files = []
            for filename in all_files:
                ifile = filename.split("/")[-1]
                ofile = os.path.join(sd_path_um, ifile)
                if os.path.islink(ofile):
                    logging.info(f"{ofile} already exists.")
                    continue
                parts = split_filename(ifile)
                if parts[0] in exclude_params:
                    continue
                ym = parts[1]
                year = int(ym.split("-")[0])
                if year < year_init:
                    continue
                if year > year_end:
                    continue
                
                logging.info(f"Create symlink: {ofile}")
                call(" ".join(["ln -s", filename, ofile]), shell=True)

    sys.exit(0)

if __name__ == "__main__":
    main()
