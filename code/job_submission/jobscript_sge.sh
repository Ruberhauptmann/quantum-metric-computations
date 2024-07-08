#$ -q idefix.q
#$ -l h_vmem=4G
#$ -pe smp 12
#$ -l h_cpu=1:00:00
#$ -M tsievers@physnet.uni-hamburg.de -m beas
#$ -cwd
#$ -S /bin/bash

module load anaconda3/2023.03

conda activate quant-met-computations

V=$1
mu=$2

clone_src = "${PWD}"

# define DSLOCKFILE & GIT ENV for job.sh
export DSLOCKFILE=${PWD}/.datalad_lock GIT_AUTHOR_NAME=$(git config user.name) GIT_AUTHOR_EMAIL=$(git config user.email) FULLJOBID="V_${V}.mu_${mu}.${JOB_ID}"
# use computation specific folder
mkdir ${HOME}//${FULLJOBID}
cd ${HOME}//${FULLJOBID}

# run things
${PWD}/code/job_submission/job.sh "${clone_src}" "${V}" "${mu}"

cd ${HOME}
chmod 777 -R ${HOME}//${FULLJOBID}
rm -fr ${HOME}//${FULLJOBID}
