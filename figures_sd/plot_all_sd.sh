#!/bin/bash

source ../setpaths.sh
source ../setenv.sh

# give ts or grid as argument to plot only timeseries or grid files

version=$1
release=$2
source_dck_list=$(readlink -f $3)

echo $source_dck_list

#p_opt=$3

mug_conf_dir_fig=${mug_config_directory}/${release}/figures_sd
script_dir=${mug_code_directory}/figures_sd
# $(readlink --canonicalize $mug_conf_dir_fig)

cd ${script_dir}

while read sid_dck; do
  log_diri=${mug_data_directory}/${version}/level2/log/${sid_dck}

  echo '${sid_dck}: start plotting'
  python ecv_reports_ts_plot_grid_sd.py ${sid_dck} $mug_conf_dir_fig/ecv_reports_ts_plot_grid_sd-all.json > ${log_diri}/ecv_reports_ts_plot_grid_sd-all.log 2>&1 &
  python ecv_reports_ts_plot_grid_sd.py ${sid_dck} $mug_conf_dir_fig/ecv_reports_ts_plot_grid_sd-optimal.json > ${log_diri}/ecv_reports_ts_plot_grid_sd-optimal.log 2>&1 &
  python nreports_dup_ts_sd.py ${sid_dck} $mug_conf_dir_fig/nreports_dup_ts_sd.json > ${log_diri}/nreports_dup_ts_sd.log 2>&1 &
  python nreports_qc_ts_sd.py ${sid_dck} $mug_conf_dir_fig/nreports_qc_ts_sd.json > ${log_diri}/nreports_qc_ts_sd.log 2>&1 & 
  python param_lat_bands_ts.py ${sid_dck} all $mug_conf_dir_fig/param_lat_bands_ts.json > ${log_diri}/param_lat_bands_all_ts.log 2>&1 &
  python param_lat_bands_ts.py ${sid_dck} optimal $mug_conf_dir_fig/param_lat_bands_ts.json > ${log_diri}/param_lat_bands_optimal_ts.log 2>&1 &
  python report_io_plot_sd.py ${sid_dck} $mug_conf_dir_fig/report_io_plot_sd.json > ${log_diri}/report_io_plot_sd.log 2>&1 & 
  
  sleep 1
  #make this more gentle for login node
done < $source_dck_list

echo "plot jobs are runnning in background!"

