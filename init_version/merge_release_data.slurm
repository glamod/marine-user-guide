#!/bin/bash
# Runs the pyscript that links the release data files to the marine user guide
# directory
#
# Calling sequence:
# ./merge_release_data.slurm version script_config_file process_list

# ------------------------------------------------------------------------------
#queue=short-serial
#t=01:00:00
#mem=100
#om=truncate
# ------------------------------------------------------------------------------
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" 
source $script_dir/../setenv.sh

#Do the sourcing before!

# Here make sure we are using fully expanded paths, as some may be passed to a config file
script_config_file=$(readlink --canonicalize $1)
process_list=$(readlink --canonicalize $2)

version=$(grep '"mug_version"' $script_config_file | cut -d':' -f2 | tr -d '", ')
data_directory=$(grep '"input_dir"' $script_config_file | cut -d':' -f2 | tr -d '", ')
mug_code_directory=$script_dir/..
mug_data_directory=$(grep '"output_dir"' $script_config_file | cut -d':' -f2 | tr -d '", ')

pyscript="$mug_code_directory/init_version/merge_release_data.py $data_directory $mug_data_directory/$version $script_config_file"
log_dir=$mug_data_directory/$version/level2/log
if [ ! -d $log_dir ]
then
  echo "LOG directory does not exist: $log_dir"
  exit
fi

echo "LOG directory is $log_dir"

for sid_dck in $(awk '{print $1}' $process_list)
do
  log_dir_sd=$log_dir/$sid_dck
  if [ ! -d $log_dir_sd ]
  then
    echo "Source-deck LOG dir does not exist: $log_dir_sd"
    exit
  fi

  J=$sid_dck
  log_file=$log_dir_sd/merge_release_data.log
  if [ -f "$log_file" ];then rm $log_file;fi
  failed_file=$log_dir_sd/merge_release_data.failed
  if [ -f "$failed_file" ];then rm $failed_file;fi
  ok_file=$log_dir_sd/merge_release_data.ok
  if [ -f "$ok_file" ];then 
    echo "$ok_file exists, proceeding to next (no rerun)"
  else
    if python $pyscript $sid_dck > $log_file; then
      mv $log_file $ok_file
    else
      mv $log_file $failed_file
    fi
  fi
done
