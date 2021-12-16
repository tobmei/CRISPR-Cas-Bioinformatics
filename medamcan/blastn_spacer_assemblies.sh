#!/bin/bash
#SBATCH --job-name=blastn_spacer
##SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
##SBATCH --spread-job
#SBATCH --exclude=ford,daimler
#SBATCH --array=0-235
#SBATCH --mem-per-cpu=1GB
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=tobias.meier@ibvt.uni-stuttgart.de
#SBATCH --output=slurm-%A_%a.out

# input directories and reads
#FILES=(/data/tobias/crispr_arrays/*_spacers.fasta)
FILES=(/data/tobias/ncbi_crispr_arrays/spacers_unique/*) # each spacer fasta is named after ncbi id without extensions
FILE="${FILES[$SLURM_ARRAY_TASK_ID]}"

BLAST_DB=/data/tobias/databases/opt_assemblies_blastdb
#BLAST_DB=/data/tobias/databases/generic_assemblies_blastdb

echo "job ID: ${SLURM_JOB_ID}"
echo "array job ID: ${SLURM_ARRAY_JOB_ID}"
echo "array task ID: ${SLURM_ARRAY_TASK_ID}"
echo "array task count: ${SLURM_ARRAY_TASK_COUNT}"
echo "array task min: ${SLURM_ARRAY_TASK_MIN}"
echo "array task max: ${SLURM_ARRAY_TASK_MAX}"
echo "file: ${FILE}"

BASE="$(basename ${FILE})"
NCBI_ID="${BASE}"
echo "ncbi id: ${NCBI_ID}"

IN_DIR=(${FILE})
OUT_DIR=(${PWD})
echo "in dir: ${IN_DIR}"
echo "out dir: ${OUT_DIR}"

#blastn --help
/tools/bin/blastn -db ${BLAST_DB}/${NCBI_ID}_blastdb -query ${FILE} -out "${NCBI_ID}_blastn_results.out" -evalue 0.01 -outfmt 6 -num_threads 12