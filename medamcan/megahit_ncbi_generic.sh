#!/bin/bash
#SBATCH --job-name=generic_assemblies
##SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
##SBATCH --spread-job
#SBATCH --exclude=ford,daimler
#SBATCH --array=0-293%15
#SBATCH --mem-per-cpu=2GB
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=tobias.meier@ibvt.uni-stuttgart.de
#SBATCH --output=slurm-%A_%a.out

# input directories and reads
#FILES=(/data/tobias/ncbi/*)
FILES=(/data/tobias/ncbi_assemblies/trimmed_reads/*)
FILE="${FILES[$SLURM_ARRAY_TASK_ID]}"
READS_R1=(${FILE}/*.sra_1.*_clean*)
READS_R2=(${FILE}/*.sra_2.*_clean*)

# get basename of reads
declare -a BASENAME_READS_R1
for f in "${READS_R1[@]}"
do
  BASENAME_READS_R1+=(/data/$(basename "$f"))
done

declare -a BASENAME_READS_R2
for f in "${READS_R2[@]}"
do
  BASENAME_READS_R2+=(/data/$(basename "$f"))
done

echo "job ID: ${SLURM_JOB_ID}"
echo "array job ID: ${SLURM_ARRAY_JOB_ID}"
echo "array task ID: ${SLURM_ARRAY_TASK_ID}"
echo "array task count: ${SLURM_ARRAY_TASK_COUNT}"
echo "array task min: ${SLURM_ARRAY_TASK_MIN}"
echo "array task max: ${SLURM_ARRAY_TASK_MAX}"
echo "file: ${FILE}"

# create comma separated string of reads for megahit
printf -v joined_R1 '%s,' "${BASENAME_READS_R1[@]}"
echo "reads R1: ${joined_R1%,}"
printf -v joined_R2 '%s,' "${BASENAME_READS_R2[@]}"
echo "reads R2: ${joined_R2%,}"

BASE="$(basename ${FILE})"
NCBI_ID="${BASE}"
echo "ncbi id: ${NCBI_ID}"

IN_DIR=(${FILE})
OUT_DIR=(${PWD})
echo "in dir: ${IN_DIR}"
echo "out dir: ${OUT_DIR}"

docker run --rm --user 10018:1000 -v ${IN_DIR}:/data -v ${OUT_DIR}:/out c3fd4c1b9681 megahit -1 ${joined_R1%,} -2 ${joined_R2%,} -t 24 -o /out/${NCBI_ID}_megahit_out
#docker run --rm --user 10018:1000 -v ${IN_DIR}:/data -v ${OUT_DIR}:/out c3fd4c1b9681 megahit -1 ${BASENAME_READS_R1[0]} -2 ${BASENAME_READS_R2[0]} -t 24 --k-min 21 --k-max 121 --k-step 10 -o /out/${NCBI_ID}_megahit_out
