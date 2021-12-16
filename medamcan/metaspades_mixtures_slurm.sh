#!/bin/bash
#SBATCH --job-name=msxlow
##SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
##SBATCH --spread-job
#SBATCH --exclude=ford,daimler,benz,maybach,tesla
#SBATCH --array=0-17%3
#SBATCH --mem-per-cpu=10GB
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=tobias.meier@ibvt.uni-stuttgart.de
#SBATCH --output=slurm-%A_%a.out

# input directories and reads
JOB_FILES=(/data/tobias/optimized_assembler/assemblies/mixture_assemblies/mix_parameters/metaspades/*)
JOB="${JOB_FILES[$SLURM_ARRAY_TASK_ID]}"

SAMPLE=nancy
#SAMPLE=bioreaktor

READS_R1_LOW=/data/tobias/${SAMPLE}/mixtures/MGV_R1_low.fastq.gz
READS_R2_LOW=/data/tobias/${SAMPLE}/mixtures/MGV_R2_low.fastq.gz
READS_R1_MID=/data/tobias/${SAMPLE}/mixtures/MGV_R1_mid.fastq.gz
READS_R2_MID=/data/tobias/${SAMPLE}/mixtures/MGV_R2_mid.fastq.gz
READS_R1_HIGH=/data/tobias/${SAMPLE}/mixtures/MGV_R1_high.fastq.gz
READS_R2_HIGH=/data/tobias/${SAMPLE}/mixtures/MGV_R2_high.fastq.gz

OUT_DIR=(${PWD})
echo "out dir: ${OUT_DIR}"
BASE="$(basename ${JOB})"

KLIST=$(cat ${JOB})

echo "job ID: ${SLURM_JOB_ID}"
echo "array job ID: ${SLURM_ARRAY_JOB_ID}"
echo "array task ID: ${SLURM_ARRAY_TASK_ID}"
echo "array task count: ${SLURM_ARRAY_TASK_COUNT}"
echo "array task min: ${SLURM_ARRAY_TASK_MIN}"
echo "array task max: ${SLURM_ARRAY_TASK_MAX}"
echo "klist: ${KLIST}"
echo "job: ${JOB}"

docker run --rm --user 10018:1000 -v ${READS_R1_LOW}:/readR1.fastq.gz -v ${READS_R2_LOW}:/readR2.fastq.gz -v ${OUT_DIR}:/out 527fa9bf0a53 spades.py --meta -1 /readR1.fastq.gz -2 /readR2.fastq.gz -t 24 -k ${KLIST} -m 240 -o /out/${BASE}
#docker run --rm --user 10018:1000 -v ${READS_R1_MID}:/readR1.fastq.gz -v ${READS_R2_MID}:/readR2.fastq.gz -v ${OUT_DIR}:/out 527fa9bf0a53 spades.py --meta -1 /readR1.fastq.gz -2 /readR2.fastq.gz -t 24 -k ${KLIST} -m 240 -o /out/${BASE}
#docker run --rm --user 10018:1000 -v ${READS_R1_HIGH}:/readR1.fastq.gz -v ${READS_R2_HIGH}:/readR2.fastq.gz -v ${OUT_DIR}:/out 527fa9bf0a53 spades.py --meta -1 /readR1.fastq.gz -2 /readR2.fastq.gz -t 24 -k ${KLIST} -m 240 -o /out/${BASE}
