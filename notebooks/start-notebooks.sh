#!/bin/bash

set -e

# Na versão 4 o comando abaixo pode ficar comantado
# jupyter lab build # Execute na primeira vez
jupyter lab --notebook-dir=$PWD --port=8389 --no-browser
# sleep 3
echo "`date` - gerando a configuração"
jupyter lab --generate-config
