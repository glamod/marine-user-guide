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


TIME='05:00:00'
NODES=1
TasksPN=12#190/GBpernode


#mem=10000
#om=truncate



if len(sys.argv)==3:
    logging.info('Reading command line arguments')
    args = sys.argv
else:
    logging.error('Need two arguments to run!')
    sys.exit(1)

#reading arguments
version=args[1]
grid_config_file=os.path.realpath(args[2])


#reading env variables
mug_data_dir = os.getenv('mug_data_directory')
mug_code_dir = os.getenv('mug_code_directory')

#building path/commands
logdir = os.path.join(mug_data_dir, version, 'level2','log')
if not os.path.isdir(logdir):
    sys.exit('Log directory not found at: {}'.format(logdir))


pyscript_grid = os.path.join(*[mug_code_dir, 'data_summaries','monthly_grids.py'])#config_file
pyscript_qi = os.path.join(*[mug_code_dir, 'data_summaries','monthly_qi.py'])

taskfile = os.path.join(logdir, 'monthly.tasks')
slurmfile = os.path.join(logdir, 'monthly.slurm')

tables = ['header', 'observations-sst', 'observations-at', 'observations-dpt', 'observations-wd', 'observations-ws', 'observations-slp']
#writing combined taskfile for grids and qi
with open(taskfile, 'w') as fn:
    for table in tables:

        logfile_grid = os.path.join(logdir,'{}-{}.log'.format(os.path.basename(grid_config_file)[:-5], table))
        successfile_grid = os.path.join(logdir,'{}-{}.success'.format(os.path.basename(grid_config_file)[:-5], table))
        failedfile_grid = os.path.join(logdir,'{}-{}.failed'.format(os.path.basename(grid_config_file)[:-5], table))
        if os.path.isfile(logfile_grid):
             logging.info('Deleting {} file for a fresh start'.format(logfile_grid))
             os.remove(logfile_grid)
        if os.path.isfile(failedfile_grid):
             logging.info('Deleting {} file for a fresh start'.format(failedfile_grid))
             os.remove(failedfile_grid)

        fn.writelines('python {0} {1} {2} > {3} 2> {3}; if [ $? -eq 0 ]; then touch {4}; else touch {5}; fi \n'.format(pyscript_grid, grid_config_file, table, logfile_grid, successfile_grid, failedfile_grid))

    for qi in ['duplicate_status', 'report_quality']:
        logfile_qi = os.path.join(logdir,'{}-{}.log'.format(os.path.basename(grid_config_file)[:-5], qi))
        successfile_qi = os.path.join(logdir,'{}-{}.success'.format(os.path.basename(grid_config_file)[:-5], qi))
        failedfile_qi = os.path.join(logdir,'{}-{}.failed'.format(os.path.basename(grid_config_file)[:-5], qi))
        if os.path.isfile(logfile_qi):
            logging.info('Deleting {} file for a fresh start'.format(logfile_qi))
            os.remove(logfile_qi)
        if os.path.isfile(failedfile_qi):
            logging.info('Deleting {} file for a fresh start'.format(failedfile_qi))
            os.remove(failedfile_qi)

        fn.writelines('python {0} {1} {2} > {3} 2> {3}; if [ $? -eq 0 ]; then touch {4}; else touch {5}; fi \n'.format(pyscript_qi, grid_config_file, qi, logfile_qi,successfile_qi, failedfile_qi))
        #grid_config==qi_config!


with open(slurmfile,'w') as fh:
    fh.writelines('#!/bin/bash\n')
    fh.writelines('#SBATCH --job-name=grid_qi.job\n')
    fh.writelines('#SBATCH --output={}/%a.out\n'.format(logdir))
    fh.writelines('#SBATCH --error={}/%a.err\n'.format(logdir))
    fh.writelines('#SBATCH --time={}\n'.format(TIME))
    fh.writelines('#SBATCH --nodes={}\n'.format(NODES))
    #fh.writelines('#SBATCH --mem={}\n'.format(MEM))
    fh.writelines('#SBATCH -A glamod\n')
    fh.writelines('module load taskfarm\n')
    fh.writelines('export TASKFARM_PPN={}\n'.format(TasksPN))
    fh.writelines('taskfarm {}\n'.format(taskfile))


logging.info('{}: launching taskfarm'.format(taskfile))
process = "jid=$(sbatch {}) && echo $jid".format(slurmfile)
jid = launch_process(process)



















