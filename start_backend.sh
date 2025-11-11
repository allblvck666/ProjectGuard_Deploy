#!/bin/bash
cd "$(dirname "$0")"
export PYTHONPATH=$PYTHONPATH:$(pwd)
uvicorn backend.main:app --host 0.0.0.0 --port 10000
