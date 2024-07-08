#!/bin/bash

V=$1
mu=$2

LOG_DIR = "${HOME}/quan-met_logs/V_${V}/mu_${mu}"
JOB_NAME = "quant-met_V_${V}_mu_${mu}"

mkdir -p "${LOG_DIR}"

qsub -o "${LOG_DIR}" -N "${JOB_NAME}" code/job_submission/jobscript_sge.sh ${V} ${mu}
