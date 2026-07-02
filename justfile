#!/usr/bin/env -S just --justfile

build:
    mkdir -p artefacts/
    python -m build --outdir artefacts/ src/shm
    python -m build --outdir artefacts/ src/tsq

install:
    pip install ./artefacts/*.whl