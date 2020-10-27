#!/bin/bash

#colors
RESET=0
BLACK=30
RED=31
GREEN=32
YELLOW=33
BLUE=34

COLOR=$YELLOW
echo -e "\e[1;${COLOR}m Running static code analysis..."
mypy sdk_solver
echo -e "\e[1;${COLOR}m Running unit tests..."
python -m pytest
echo -e "\e[1;${COLOR}m Done"


