#!/bin/bash

source ../setpaths.sh
source ../setenv.sh

# give ts or grid as argument to plot only timeseries or grid files

version=$1
release=$2
p_opt=$3
mug_conf_dir_fig=${mug_config_directory}/${release}/figures
script_dir=${mug_code_directory}/figures
# $(readlink --canonicalize $mug_conf_dir_fig)
log_dir=${mug_data_directory}/${version}/level2/log

cd ${script_dir}

if [ "$p_opt" != "grid" ]
then
  echo 'plotting time series'
  python3 nreports_ts_plot.py ${mug_conf_dir_fig}/nreports_ts_plot.json > ${log_dir}/nreports_ts_plot.log 2>&1 &
  python3 duplicate_status_ts_plot.py ${mug_conf_dir_fig}/duplicate_status_ts_plot.json  > ${log_dir}/duplicate_status_ts_plot.log 2>&1 &
  python3 report_quality_ts_plot.py  ${mug_conf_dir_fig}/report_quality_ts_plot.json > ${log_dir}/report_quality_ts_plot.log 2>&1 &
fi

if [ "$p_opt" != "ts" ]
then
  echo 'plotting grid files'
  python3 nreports_hovmoller_plot.py ${mug_conf_dir_fig}/nreports_hovmoller_plot.json  > ${log_dir}/nreports_hovmoller_plot.log 2>&1 &
  python3 ecv_coverage_ts_plot_grid.py ${mug_conf_dir_fig}/ecv_coverage_ts_plot_grid.json  > ${log_dir}/ecv_coverage_ts_plot_grid.log 2>&1 &
  python3 nreports_and_nmonths_maps.py ${mug_conf_dir_fig}/nreports_and_nmonths_maps.json  > ${log_dir}/nreports_and_nmonths_maps.log 2>&1 &
  python3 mean_observed_value_maps.py ${mug_conf_dir_fig}/mean_observed_value_maps.json  > ${log_dir}/mean_observed_value_maps.log 2>&1 &
fi

echo "plot jobs are runnning in background!"

