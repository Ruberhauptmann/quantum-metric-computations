#!/bin/bash

V=$1
mu=$2

job_name="quant-met_V_${V}_mu_${mu}"
log_dir="${HOME}/quant-met_logs/"

mkdir -p "${log_dir}"

sbatch -o "${log_dir}/${job_name}_%j.out" -J "${job_name}" code/job_submission/jobscript_slurm.sh ${V} ${mu}
