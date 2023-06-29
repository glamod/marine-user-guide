#!/bin/bash
python $code_directory//marine-user-guide/figures/nreports_ts_plot.py nreports_ts_plot.json
python $code_directory//marine-user-guide/figures/duplicate_status_ts_plot.py duplicate_status_ts_plot.json 
python $code_directory//marine-user-guide/figures/report_quality_ts_plot.py report_quality_ts_plot.json 
python $code_directory//marine-user-guide/figures/nreports_hovmoller_plot.py nreports_hovmoller_plot.json 
python $code_directory//marine-user-guide/figures/ecv_coverage_ts_plot_grid.py ecv_coverage_ts_plot_grid.json 
python $code_directory//marine-user-guide/figures/nreports_and_nmonths_maps.py nreports_and_nmonths_maps.json 
python $code_directory//marine-user-guide/figures/mean_observed_value_maps.py mean_observed_value_maps.json 
