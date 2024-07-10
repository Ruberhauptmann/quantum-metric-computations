#!/bin/bash -x
#SBATCH --time=2:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=short-nompi
#SBATCH --nodes=1
#SBATCH --mail-user=tsievers@physnet.uni-hamburg.de
#SBATCH --mail-type=ALL

module purge
module load anaconda3/2023.03
conda activate quant-met-computations

python3 -m cProfile -o profiling/profile_0_0_4  code/minimise/minimise.py --v 1.0 --mu 0.0 --nprocs 1 --path test_results
