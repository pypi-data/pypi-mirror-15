#!/usr/bin/env bash

export THEANO_FLAGS='mode=FAST_RUN,device=gpu,nvcc.fastmath=True,floatX=float32,allow_gc=True,openmp=True'
export OMP_NUM_THREADS=`nproc`
export PYTHONPATH="$PYTHONPATH:."
