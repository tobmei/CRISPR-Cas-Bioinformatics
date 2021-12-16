#!/bin/bash
#SBATCH --job-name=makeblastdb
##SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
##SBATCH --spread-job
##SBATCH --exclude=ford,daimler
#SBATCH --array=0-293
#SBATCH --mem-per-cpu=20GB
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=tobias.meier@ibvt.uni-stuttgart.de
#SBATCH --output=slurm-%A_%a.out

# input data
FILES=(/data/tobias/ncbi_assemblies/opt_assemblies/*)
#FILES=(/data/tobias/ncbi_assemblies/generic_assemblies/*)
FILE="${FILES[$SLURM_ARRAY_TASK_ID]}"

echo "job ID: ${SLURM_JOB_ID}"
echo "array job ID: ${SLURM_ARRAY_JOB_ID}"
echo "array task ID: ${SLURM_ARRAY_TASK_ID}"
echo "array task count: ${SLURM_ARRAY_TASK_COUNT}"
echo "array task min: ${SLURM_ARRAY_TASK_MIN}"
echo "array task max: ${SLURM_ARRAY_TASK_MAX}"
echo "file: ${FILE}"

BASE="$(basename ${FILE})"
echo "base: ${BASE}"

IN_DIR=(${FILE})
OUT_DIR=(${PWD})
echo "in dir: ${IN_DIR}"
echo "out dir: ${OUT_DIR}"

#blastn --help
makeblastdb -in ${IN_DIR} -dbtype nucl -parse_seqids -out ${BASE}_blastdb -title ${BASE}_blastdb
