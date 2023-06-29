# load python module
#module load jaspy/3.7/r20181219

# WATCH THIS HARCODING UNTIL WE DECIDE WHAT TO DO WITH REPOS AND ENVS!
#pyEnvironment_directory=$mug_code_directory/env/mug_env
pyEnvironment_directory=/ichec/work/glamod/marine-user-guide.2022/env/env1

# Activate python environment and add jaspy3.7 path to LD_LIBRARY_PATH so that cartopy and other can find the geos library
source activate $pyEnvironment_directory
export PYTHONPATH="$mug_code_directory:${PYTHONPATH}"
#export LD_LIBRARY_PATH=/apps/contrib/jaspy/miniconda_envs/jaspy3.7/m3-4.5.11/envs/jaspy3.7-m3-4.5.11-r20181219/lib/:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/ichec/packages/conda/2/lib/:$LD_LIBRARY_PATH
echo "Python environment loaded from: $pyEnvironment_directory"
