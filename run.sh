#!/bin/bash

s_flag=false
d_flag=false

if [ ! -d "Projects" ]; then
    mkdir Projects
fi

while getopts 'sdc' flag; do
    case "${flag}" in
        s) s_flag=true ;;
        d) d_flag=true ;;
        c) rm -rf Projects ;;
    esac
done

if $s_flag; then
    echo "Scrapeing projects"
    py WebScraper.py
fi

if $d_flag; then
    echo "Embeding projects"
    py VectorDB.py
fi
