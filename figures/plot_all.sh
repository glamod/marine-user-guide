#!/bin/bash

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source $script_dir/../setenv.sh

# give ts or grid as argument to plot only timeseries or grid files

script_config_file=$(readlink --canonicalize $1)
version=$(grep '"mug_version"' $script_config_file | cut -d':' -f2 | tr -d '", ')
release=$(grep '"glamod_release"' $script_config_file | cut -d':' -f2 | tr -d '", ')
mug_data_directory=$(grep '"output_dir"' $script_config_file | cut -d':' -f2 | tr -d '", ') 
mug_code_directory=$script_dir/..
mug_conf_dir_fig=$mug_code_directory/config/$release/figures/
p_opt=$2
script_dir=${mug_code_directory}/figures
log_dir=${mug_data_directory}/${version}/level2/log
file_path=${mug_data_directory}/${version}/level2/reports

if [ "$p_opt" != "grid" ]
then
  echo 'plotting time series'
  python ${script_dir}/nreports_ts_plot.py ${mug_conf_dir_fig}/nreports_ts_plot.json ${file_path} > ${log_dir}/nreports_ts_plot.log 2>&1 &
  python ${script_dir}/duplicate_status_ts_plot.py ${mug_conf_dir_fig}/duplicate_status_ts_plot.json ${file_path} > ${log_dir}/duplicate_status_ts_plot.log 2>&1 &
  python ${script_dir}/report_quality_ts_plot.py  ${mug_conf_dir_fig}/report_quality_ts_plot.json ${file_path} > ${log_dir}/report_quality_ts_plot.log 2>&1 &
fi

if [ "$p_opt" != "ts" ]
then
  echo 'plotting grid files'
  python ${script_dir}/nreports_hovmoller_plot.py ${mug_conf_dir_fig}/nreports_hovmoller_plot.json ${file_path} > ${log_dir}/nreports_hovmoller_plot.log 2>&1 &
  python ${script_dir}/ecv_coverage_ts_plot_grid.py ${mug_conf_dir_fig}/ecv_coverage_ts_plot_grid.json ${file_path} > ${log_dir}/ecv_coverage_ts_plot_grid.log 2>&1 &
  python ${script_dir}/nreports_and_nmonths_maps.py ${mug_conf_dir_fig}/nreports_and_nmonths_maps.json ${file_path} > ${log_dir}/nreports_and_nmonths_maps.log 2>&1 &
  python ${script_dir}/mean_observed_value_maps.py ${mug_conf_dir_fig}/mean_observed_value_maps.json ${file_path} > ${log_dir}/mean_observed_value_maps.log 2>&1 &
fi

echo "plot jobs are runnning in background!"

