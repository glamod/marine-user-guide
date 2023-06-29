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


TIME='00:59:00'
NODES=1
TasksPN=19
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
grid_config_file=os.path.realpath(args[2])
sidck_file=os.path.realpath(args[3])

#reading env variables
mug_data_dir = os.getenv('mug_data_directory')
mug_code_dir = os.getenv('mug_code_directory')

#building path/commands
level2dir = os.path.join(mug_data_dir, version, 'level2')
logdir = os.path.join(level2dir,'log')
if not os.path.isdir(logdir):
    sys.exit('Log directory not found at: {}'.format(logdir))


pyscript_grid = os.path.join(mug_code_dir, 'data_summaries_sd','monthly_grids_sd.py')
pyscript_qi = os.path.join(mug_code_dir, 'data_summaries_sd','monthly_qi_sd.py')
pyscript_io = os.path.join(mug_code_dir, 'data_summaries_sd','report_io_sd.py')

with open(grid_config_file,'r') as fO:
    config = json.load(fO)

filterqc=config["id_out"]

taskfile = os.path.join(logdir, 'monthly_sd_{}.tasks'.format(filterqc))
slurmfile = os.path.join(logdir, 'monthly_sd_{}.slurm'.format(filterqc))

tables = ['header', 'observations-sst', 'observations-at', 'observations-dpt', 'observations-wd', 'observations-ws', 'observations-slp']
#writing combined taskfile for grids and qi

with open(sidck_file, 'r') as sidck_fh:
    with open(taskfile, 'w') as fn:
        for sidck in sidck_fh:
            sid_dck = sidck.rstrip()
            logdir_sidck=os.path.join(logdir, sid_dck)
            logging.info(repr(sidck))
            if not os.path.isdir(logdir_sidck):
                 sys.exit('Log directory not found at: {}'.format(logdir_sidck))

            for table in tables:
                logfile_grid = os.path.join(logdir_sidck,'{}-{}.log'.format(os.path.basename(grid_config_file)[:-5], table))
                successfile_grid = os.path.join(logdir_sidck,'{}-{}.success'.format(os.path.basename(grid_config_file)[:-5], table))
                failedfile_grid = os.path.join(logdir_sidck,'{}-{}.failed'.format(os.path.basename(grid_config_file)[:-5], table))
                if os.path.isfile(logfile_grid):
                    logging.info('Deleting {} file for a fresh start'.format(logfile_grid))
                    os.remove(logfile_grid)
                if os.path.isfile(failedfile_grid):
                    logging.info('Deleting {} file for a fresh start'.format(failedfile_grid))
                    os.remove(failedfile_grid)
                if os.path.isfile(successfile_grid):
                    logging.info('{} file exists, no re-run!'.format(successfile_grid))
                else:
                    fn.writelines('python {0} {1} {2} {3} > {4} 2>&1; if [ $? -eq 0 ]; then touch {5}; else touch {6}; fi \n'.format(pyscript_grid,sid_dck, table, grid_config_file, logfile_grid, successfile_grid, failedfile_grid))

            for qi in ['duplicate_status', 'report_quality']:
                logfile_qi = os.path.join(logdir_sidck,'{}-{}.log'.format(os.path.basename(grid_config_file)[:-5], qi))
                successfile_qi = os.path.join(logdir_sidck,'{}-{}.success'.format(os.path.basename(grid_config_file)[:-5], qi))
                failedfile_qi = os.path.join(logdir_sidck,'{}-{}.failed'.format(os.path.basename(grid_config_file)[:-5], qi))
                if os.path.isfile(logfile_qi):
                    logging.info('Deleting {} file for a fresh start'.format(logfile_qi))
                    os.remove(logfile_qi)
                if os.path.isfile(failedfile_qi):
                    logging.info('Deleting {} file for a fresh start'.format(failedfile_qi))
                    os.remove(failedfile_qi)
                if os.path.isfile(successfile_qi):
                    logging.info('{} file exists, no re-run!'.format(successfile_qi))
                else:
                    fn.writelines('python {0} {1} {2} {3} > {4} 2>&1; if [ $? -eq 0 ]; then touch {5}; else touch {6}; fi \n'.format(pyscript_qi, sid_dck, qi, grid_config_file, logfile_qi, successfile_qi, failedfile_qi))
                    #grid_config==qi_config!

            if filterqc=='all':
                logfile_io = os.path.join(logdir_sidck,'{}-{}.log'.format(os.path.basename(grid_config_file)[:-5], 'report_io'))
                successfile_io = os.path.join(logdir_sidck,'{}-{}.success'.format(os.path.basename(grid_config_file)[:-5],  'report_io'))
                failedfile_io = os.path.join(logdir_sidck,'{}-{}.failed'.format(os.path.basename(grid_config_file)[:-5],  'report_io'))
                if os.path.isfile(logfile_io):
                    logging.info('Deleting {} file for a fresh start'.format(logfile_io))
                    os.remove(logfile_io)
                if os.path.isfile(failedfile_io):
                    logging.info('Deleting {} file for a fresh start'.format(failedfile_io))
                    os.remove(failedfile_io)
                if os.path.isfile(successfile_io):
                    logging.info('{} file exists, no re-run!'.format(successfile_io))
                else:
                    fn.writelines('python {0} {1} {2} > {3} 2>&1; if [ $? -eq 0 ]; then touch {4}; else touch {5}; fi \n'.format(pyscript_io, sid_dck, grid_config_file, logfile_io, successfile_io, failedfile_io))
   





with open(slurmfile,'w') as fh:
    fh.writelines('#!/bin/bash\n')
    fh.writelines('#SBATCH --job-name=grid_qi_sd.job\n')
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



















