declare -a arr=(
    "exchange"
    "x264"
    "gcc"
    "nab"
    "imagick"
    "lbm"
    "mixed_workloads"
)

summary_file="temp_traces/summary"
> $summary_file
for benchmark in "${arr[@]}"
do
    echo "$benchmark" >> $summary_file
    for weight in power_traces/$benchmark/*
    do
        val=${weight##*/}
	echo "$val" >> $summary_file
        for policy in temp_traces/*/
        do
            echo "$policy:" >> $summary_file
	    tail $policy$benchmark/$val/log -n 3 | head -n 2 >> $summary_file
        done
	echo >> $summary_file
    done
    echo >> $summary_file
done
