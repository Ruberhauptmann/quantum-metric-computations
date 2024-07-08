#!/bin/bash

# This is the common jobscript for all clusters.

# fail whenever something is fishy, use -x to get verbose logfiles
set -e -u -x

# we pass arbitrary arguments via job scheduler and can use them as variables
dssource="$1"
V="$2"
mu="$3"
nprocs="$4"

# go into unique location
#cd /tmp
# clone the analysis dataset. flock makes sure that this does not interfere
# with another job finishing and pushing results back at the same time
flock --verbose "${DSLOCKFILE}" datalad clone "${dssource}" ds
cd ds

# announce the clone to be temporary
git annex dead here
# checkout a unique branch
git checkout -b "job-${FULLJOBID}"

# run the job
LC_NUMERIC="en_US.UTF-8" printf -v result_path "minimise_results/%.2f/%.2f" $V $mu
datalad run \
  -m "Compute V=${V}, mu=${mu}" \
  --explicit \
  -o "${result_path}" \
  "python code/minimise/minimise.py --nprocs ${nprocs}  --mu ${mu} --v ${V} --path ${result_path}"

# push, with filelocking as a safe-guard
flock --verbose "${DSLOCKFILE}" datalad push --to origin

# Done - job handler should clean up workspace
echo SUCCESS
