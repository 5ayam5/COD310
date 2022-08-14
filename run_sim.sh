declare -a arr=(
    "exchange"
    "x264"
    "gcc"
    "nab"
    "imagick"
    "lbm"
    "mixed_workloads"
)

for POLICY in BASELINE GREEDY KNAPSACK
do
    echo "$POLICY"
    cd hotspot/hotspot_tool/
    make clean > /dev/null 2>&1
    make POLICY=$POLICY > /dev/null 2>&1
    cd ../../
    for benchmark in "${arr[@]}"
    do
        echo "  $benchmark"
        for weight in power_traces/$benchmark/*
        do
            echo "    $weight"
            cp $weight/sim.out hotspot/sim128_3D_run.out
            cp $weight/log hotspot/tmp128_3D_run

            cd hotspot/
            make run file=run arch=5 > /dev/null 2> log
            cd ../
            mkdir -p temp_traces/$POLICY/$benchmark/${weight##*/}
            cp hotspot/log temp_traces/$POLICY/$benchmark/${weight##*/}
            cp -r hotspot/run/3D/. temp_traces/$POLICY/$benchmark/${weight##*/}
        done
    done
done
