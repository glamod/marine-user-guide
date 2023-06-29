#!/bin/bash python3

#make sure setpath.sh and setenv.sh are sourced before

import sys
import os
import json
import subprocess
import logging

#%%------------------------------------------------------------------------------

def launch_process(process):

    proc = subprocess.Popen([process],shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    jid_by, err = proc.communicate()
    if len(err)>0:
        logging.error('Error launching process. Exiting')
        logging.info('Error is: {}'.format(err))
        sys.exit(1)
    jid = jid_by.decode('UTF-8').rstrip()

    return jid.split(' ')[-1]

#%%------------------------------------------------------------------------------

logging.basicConfig(format='%(levelname)s\t[%(asctime)s](%(filename)s)\t%(message)s',
                    level=logging.INFO,datefmt='%Y%m%d %H:%M:%S',filename=None)

#%%------------------------------------------------------------------------------


TIME='02:00:00'
NODES=1
TasksPN=20
#190/GBpernode


#mem=10000
#om=truncate



if len(sys.argv)==4:
    logging.info('Reading command line arguments')
    args = sys.argv
else:
    logging.error('Need exactly three arguments to run')
    sys.exit(1)


#reading arguments
version=args[1]
release=args[2]
sidck_file=os.path.realpath(args[3])

#reading env variables
mug_config_dir = os.getenv('mug_config_directory')
mug_code_dir = os.getenv('mug_code_directory')
mug_data_dir = os.getenv('mug_data_directory')

#building path/commands
#level2dir = os.path.join(mug_data_dir, version, 'level2')
log_dir = os.path.join(mug_data_dir, version, 'level2', 'log')
plot_code_dir = os.path.join(mug_code_dir, 'figures_sd')

if not os.path.isdir(log_dir):
    sys.exit('Log directory not found at: {}'.format(log_dir))
if not os.path.isfile(sidck_file):
    sys.exit('List file not found at: {}'.format(sidck_file))

mug_config_dir_fig = os.path.join(mug_config_dir, release, 'figures_sd')

taskfile = os.path.join(log_dir, 'plot_sd.tasks')
slurmfile = os.path.join(log_dir, 'plot_sd.slurm')

with open(sidck_file, 'r') as sidck_fh:
    with open(taskfile, 'w') as fn:
        for sidck in sidck_fh:
            sid_dck = sidck.rstrip()
            log_diri = os.path.join(log_dir, sid_dck)
            logging.info(repr(sid_dck))
            if not os.path.isdir(log_diri):
                 sys.exit('Log directory not found at: {}'.format(log_diri))
            fn.writelines('python3 {0}/ecv_reports_ts_plot_grid_sd.py {1} {2}/ecv_reports_ts_plot_grid_sd-all.json > {3}/ecv_reports_ts_plot_grid_sd-all.log 2>&1 \n'.format(plot_code_dir, sid_dck, mug_config_dir_fig, log_diri))
            fn.writelines('python3 {0}/ecv_reports_ts_plot_grid_sd.py {1} {2}/ecv_reports_ts_plot_grid_sd-optimal.json > {3}/ecv_reports_ts_plot_grid_sd-optimal.log 2>&1 \n'.format(plot_code_dir, sid_dck, mug_config_dir_fig, log_diri))
            fn.writelines('python3 {0}/nreports_dup_ts_sd.py {1} {2}/nreports_dup_ts_sd.json > {3}/nreports_dup_ts_sd.log 2>&1 \n'.format(plot_code_dir, sid_dck, mug_config_dir_fig, log_diri))
            fn.writelines('python3 {0}/nreports_qc_ts_sd.py {1} {2}/nreports_qc_ts_sd.json > {3}/nreports_qc_ts_sd.log 2>&1 \n'.format(plot_code_dir, sid_dck, mug_config_dir_fig, log_diri))
            fn.writelines('python3 {0}/param_lat_bands_ts.py {1} all {2}/param_lat_bands_ts.json > {3}/param_lat_bands_all_ts.log 2>&1 \n'.format(plot_code_dir, sid_dck, mug_config_dir_fig, log_diri))
            fn.writelines('python3 {0}/param_lat_bands_ts.py {1} optimal {2}/param_lat_bands_ts.json > {3}/param_lat_bands_optimal_ts.log 2>&1 \n'.format(plot_code_dir, sid_dck, mug_config_dir_fig, log_diri))
            fn.writelines('python3 {0}/report_io_plot_sd.py {1} {2}/report_io_plot_sd.json > {3}/report_io_plot_sd.log 2>&1 \n'.format(plot_code_dir, sid_dck, mug_config_dir_fig, log_diri))
            
with open(slurmfile,'w') as fh:
    fh.writelines('#!/bin/bash\n')
    fh.writelines('#SBATCH --job-name=grid_qi_sd.job\n')
    fh.writelines('#SBATCH --output={}/%a.out\n'.format(log_dir))
    fh.writelines('#SBATCH --error={}/%a.err\n'.format(log_dir))
    fh.writelines('#SBATCH --time={}\n'.format(TIME))
    fh.writelines('#SBATCH --nodes={}\n'.format(NODES))
    #fh.writelines('#SBATCH --mem={}\n'.format(MEM))
    fh.writelines('#SBATCH -A glamod\n')
    fh.writelines('module load taskfarm\n')
    fh.writelines('export TASKFARM_PPN={}\n'.format(TasksPN))
    fh.writelines('export TASKFARM_GROUP=7\n')
    fh.writelines('taskfarm {}\n'.format(taskfile))


logging.info('{}: launching taskfarm'.format(taskfile))
process = "jid=$(sbatch {}) && echo $jid".format(slurmfile)
jid = launch_process(process)



















