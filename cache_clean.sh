#!/bin/bash
# set -euxo pipefail

echo -e "\033[1mClean Python caches\033[m"
pyclean -vvv .

echo -e "\033[1mClean pytest caches\033[m"
find . -type d -name  ".pytest_cache" -exec rm -r {} +

echo -e "\033[1mClean mypy caches\033[m"
find . -type d -name  ".mypy_cache" -exec rm -r {} +
