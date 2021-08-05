#!/bin/bash

function envelope {
    python3 demo/envelope/extremums.py
    python3 demo/envelope/hilbert_digital_filter.py
}

function flow {
    python3 demo/flow/add_remove_nodes.py
    python3 demo/flow/basic.py
    python3 demo/flow/generator.py
    python3 demo/flow/get_plan_from_dict.py
    python3 demo/flow/hooks.py
    python3 demo/flow/map.py
    python3 demo/flow/online.py
    python3 demo/flow/pack.py
    python3 demo/flow/select.py
    python3 demo/flow/work.py
}

function modulation {
    python3 demo/modulation/am.py
    python3 demo/modulation/fm.py
    python3 demo/modulation/harmonic.py
    python3 demo/modulation/freq_demod.py
}

function player {
    python3 demo/player/csv_file.py
    python3 demo/player/random_numbers.py
}

function prony {
    python3 demo/prony/prony.py
}

function spectran {
    python3 demo/spectran/amplitude_spectrum.py
}

function trend {
    python3 demo/trend/smooth.py
}

function show_menu {
    echo "1 - envelope"
    echo "2 - flow"
    echo "3 - modulation"
    echo "4 - player"
    echo "5 - prony"
    echo "6 - spectran"
    echo "7 - trend"
    echo "8 - all"
    echo "0 - exit"
}

function run_demo_pack {
    KEY=$1

    case $KEY in
        1)
            envelope
            ;;
        2)
            flow
            ;;
        3)
            modulation
            ;;
        4)
            player
            ;;
        5)
            prony
            ;;
        6)
            spectran
            ;;
        7)
            trend
            ;;
        8)
            envelope
            flow
            modulation
            player
            prony
            spectran
            trend
            ;;
    esac
}

n=1
while [ $n != 0 ]
do
    show_menu
    read -p "Input n: " n
    if [ $n != 0 ]; then
        run_demo_pack $n
        echo "press Enter to continue"
        read
    fi
done
