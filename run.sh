#!/bin/bash

s_flag=false
d_flag=false
a_flag=false

if [ ! -d "Projects" ]; then
    mkdir Projects
fi

while getopts 'sdca' flag; do
    case "${flag}" in
        s) s_flag=true ;;
        d) d_flag=true ;;
        a) a_flag=true ;;
        c)
            if [ $OPTARG == "projects" ]; then
                echo "removing projects"
                rm -rf Projects
            elif [ $OPTARG == "db" ]; then
                echo "removing embeddings"
                rm -rf chromadb
            else
                error "Unexpected option ${OPTIONS}"
            fi
            ;;
    esac
done

if $s_flag; then
    echo "Scrapeing projects"
    py -u WebScraper.py > scraper.log
fi

if $d_flag; then
    echo "Embeding projects"
    py -u VectorDB.py > vectors.log
fi

if $a_flag; then
    echo "starting api"
    uvicorn api:app --reload
fi
