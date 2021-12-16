#!/bin/bash
#SBATCH --job-name=classify_kraken2
##SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --spread-job
#SBATCH --exclude=daimler
#SBATCH --array=0-293%2
#SBATCH --mem-per-cpu=40GB
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=tobias.meier@ibvt.uni-stuttgart.de
#SBATCH --output=slurm-%A_%a.out

# input data
FILES=(/data/tobias/optimized_assembler/assemblies/generic_assemblies/*)
FILES=(/data/tobias/optimized_assembler/assemblies/opt_assemblies/*)
#FILES=(/data/tobias/optimized_assembler/assemblies/generic_assemblies/SRP259*)
DB=/data/tobias/databases/krakendb
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

docker run --rm --user 10018:1000 -v ${FILE}:/input -v ${OUT_DIR}:/output -v ${DB}:/db b891577959b6 kraken2 --db db --output /output/"${BASE}"_output --report /output/"${BASE}"_report /input/final.contigs.fa