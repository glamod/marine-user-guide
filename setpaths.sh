#data_directory=/gws/nopw/j04/glamod_marine/data
#data_directory=/work/scratch-nopw/aanderss/glamod_marine/data
export data_directory=/ichec/work/glamod/data/marine
#code_directory=/gws/smf/j04/c3s311a_lot2/code/marine_code
#code_directory=/home/users/aanderss/mug/code/marine_code/
export code_directory=/ichec/work/glamod/marine-user-guide.2022

export mug_data_directory=$data_directory/marine-user-guide.2022
export mug_code_directory=$code_directory
export mug_config_directory=$mug_code_directory/config

echo 'Release data directory is:             '$data_directory
echo 'Marine User guide data directory is:   '$mug_data_directory
echo 'Marine User guide code directory is:   '$mug_code_directory
echo 'Marine User guide config directory is: '$mug_config_directory

