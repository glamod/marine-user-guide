#!/bin/bash
source ../setpaths.sh

sd_dck_list=$mug_config_directory/v7/mug_list_v7.txt
mugdata=$mug_data_directory/v7/level2
r1=$data_directory/release_4.0/ICOADS_R3.0.0T/level2
r2=$data_directory/release_3.0.2/ICOADS_R3.0.2T_NRT/level2

for sd in $(awk '{print $0}' $sd_dck_list)
do

	nheader_mug=$(ls -Ubd1 $mugdata/$sd/header* 2> /dev/null | wc -l)
	nheader_r1=$(ls -Ubd1 $r1/$sd/header* 2> /dev/null | wc -l)
	nheader_r2=$(ls -Ubd1 $r2/$sd/header* 2> /dev/null | wc -l)
	echo "CHECKING $sd: $nheader_mug $nheader_r1 $nheader_r2"
	num=$((nheader_r1 + nheader_r2))

if (( nheader_mug != num ))
then
	echo "    ERROR $sd: numbers don't match"
fi
done
