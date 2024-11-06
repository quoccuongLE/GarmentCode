#!/bin/bash
VENV_DIR=${1:-".venv/garmentcode"}
if [ -f lock.conda.yaml ]; then
    conda env create -f lock.conda.yaml --prefix $VENV_DIR
else
    conda env create -f conda.yaml --prefix $VENV_DIR
    if [ -d ../NvidiaWarp-GarmentCode ]; then
        $VENV_DIR/bin/python -m pip install -e ../NvidiaWarp-GarmentCode
    else
        echo ../NvidiaWarp-GarmentCode not found!
        echo Please install the project from Github
        echo "cd ..; git clone git@github.com:maria-korosteleva/NvidiaWarp-GarmentCode.git"
    fi
fi
