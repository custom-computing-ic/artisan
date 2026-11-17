#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

build_and_publish() {
    local python_version="$1"

    echo "[i] Building and publishing Python ${python_version}"
    bash conda/conda.env.build "$python_version"
    bash conda/conda.env.publish "$python_version"
}

conda build purge-all

for version in 3.10 3.11 3.12 3.14; do
    build_and_publish "$version"
done

conda build purge-all
