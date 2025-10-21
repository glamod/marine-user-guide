# -*- coding: utf-8 -*-
""" Marine User Guide configuration setup

This script creates the data configuration of the Marine User Guide by
merging the level2 configuration files of the marine data releases that 
together are a snapshot of the marine data available in the CDS.

The user is prompted to input the following information for every data release:
    
    * Release name: directory name for the release in the marine file system
    * Dataset name: directory of the original dataset within the release
    * Release level2 file: the path to the release level2 file


On merging releases, this script will:
    
    * Raise a warning if the exclude tag for a source-deck differs 
    between data releases
    * Ignore a source-deck if it has been excluded from delivery in the data 
    releases
    * Compute the merged initial and final year.
    
This script outputs a file with the information merged (mug_config.json) a list of all included DCK-SID names (mug_list_full.txt) to the path 
indicated by the user.
    
This file can also be imported as a module and contains the following
functions:
    * get_releases - prompts the user to give release information and returns
    it
    * main - the main function of the script
"""

import sys
import json
import os
import shutil


def main():
    init_dir = os.path.dirname(os.path.abspath(__file__))
    release = input("Input name of release (no path: release_8.0): ")
    config_dir = os.path.join(init_dir, "..", "config", release)
    mug_config_src = os.path.join(config_dir, "mug_config.json")

    with open(mug_config_src) as cfg:
        mug_config = json.load(cfg)
    
    mug_dir = mug_config["output_dir"]
    mug_v = mug_config["mug_version"]
    mug_dst = os.path.join(mug_dir, mug_v)

    print(f"Make directory: {mug_dst}")
    os.makedirs(mug_dir, exist_ok=True)
    os.makedirs(mug_dst, exist_ok=True)

    mug_config_dst = os.path.join(mug_dst, f"mug_config.json")
    mug_list_src = os.path.join(config_dir, f"mug_list_full.txt")
    mug_list_dst = os.path.join(mug_dst, f"mug_list_full.txt")
    print(f"Create MUG files: {mug_config_dst} and {mug_list_dst}")
    shutil.copy(mug_config_src, mug_config_dst)
    shutil.copy(mug_list_src, mug_list_dst)

    
if __name__ == "__main__":
    main()
