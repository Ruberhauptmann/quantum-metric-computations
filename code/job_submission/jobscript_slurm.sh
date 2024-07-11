#!/bin/bash -x
#SBATCH --time=3:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --partition=short-nompi
#SBATCH --nodes=1
#SBATCH --mail-user=tsievers@physnet.uni-hamburg.de
#SBATCH --mail-type=ALL

module purge
module load anaconda3/2023.03
conda activate quant-met-computations

V=$1
mu=$2

clone_src="${PWD}"

# define DSLOCKFILE & GIT ENV for job.sh
export DSLOCKFILE=${PWD}/.datalad_lock GIT_AUTHOR_NAME=$(git config user.name) GIT_AUTHOR_EMAIL=$(git config user.email) FULLJOBID="V_${V}.mu_${mu}.${SLURM_JOB_ID}"
# use computation specific folder
mkdir ${HOME}//${FULLJOBID}
cd ${HOME}//${FULLJOBID}

# run things
${clone_src}/code/job_submission/job.sh "${clone_src}" "${V}" "${mu}" "${SLURM_JOB_CPUS_PER_NODE}"

cd ${HOME}
chmod 777 -R ${HOME}//${FULLJOBID}
rm -fr ${HOME}//${FULLJOBID}
