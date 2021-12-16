#!/bin/bash
#SBATCH --job-name=megahit_mixtures_low
##SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
##SBATCH --spread-job
##SBATCH --exclude=ford,daimler
#SBATCH --array=0-143
#SBATCH --mem-per-cpu=2GB
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=tobias.meier@ibvt.uni-stuttgart.de
#SBATCH --output=slurm-%A_%a.out

# input directories and reads
JOB_FILES=(/data/tobias/optimized_assembler/assemblies/mixture_assemblies/mix_parameters/megahit/*)
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

KMIN=$(awk '/^kmin/{print $2}' ${JOB})
KMAX=$(awk '/^kmax/{print $2}' ${JOB})
KSTEP=$(awk '/^kstep/{print $2}' ${JOB})
PRUNE=$(awk '/^prunelevel/{print $2}' ${JOB})
BUBBLE=$(awk '/^bubble/{print $2}' ${JOB})
CL=$(awk '/^cleaningrounds/{print $2}' ${JOB})

echo "job ID: ${SLURM_JOB_ID}"
echo "array job ID: ${SLURM_ARRAY_JOB_ID}"
echo "array task ID: ${SLURM_ARRAY_TASK_ID}"
echo "array task count: ${SLURM_ARRAY_TASK_COUNT}"
echo "array task min: ${SLURM_ARRAY_TASK_MIN}"
echo "array task max: ${SLURM_ARRAY_TASK_MAX}"
echo "kmin: ${KMIN}"
echo "kmax: ${KMAX}"
echo "kstep: ${KSTEP}"
echo "prunelevel: ${PRUNE}"
echo "bubble: ${BUBBLE}"
echo "cleaning rounds: ${CL}"
echo "job: ${JOB}"

docker run --rm --user 10018:1000 -v ${READS_R1_LOW}:/readR1 -v ${READS_R2_LOW}:/readR2 -v ${OUT_DIR}:/out c3fd4c1b9681 megahit -1 /readR1 -2 /readR2 -t 24 --k-min ${KMIN} --k-max ${KMAX} --k-step ${KSTEP} --bubble-level ${BUBBLE} --prune-level ${PRUNE} --cleaning-rounds ${CL} -o /out/${BASE}_megahit_out
#docker run --rm --user 10018:1000 -v ${READS_R1_MID}:/readR1 -v ${READS_R2_MID}:/readR2 -v ${OUT_DIR}:/out c3fd4c1b9681 megahit -1 /readR1 -2 /readR2 -t 24 --k-min ${KMIN} --k-max ${KMAX} --k-step ${KSTEP} --bubble-level ${BUBBLE} --prune-level ${PRUNE} -o /out/${BASE}_megahit_out
#docker run --rm --user 10018:1000 -v ${READS_R1_HIGH}:/readR1 -v ${READS_R2_HIGH}:/readR2 -v ${OUT_DIR}:/out c3fd4c1b9681 megahit -1 /readR1 -2 /readR2 -t 24 --k-min ${KMIN} --k-max ${KMAX} --k-step ${KSTEP} --bubble-level ${BUBBLE} --prune-level ${PRUNE} -o /out/${BASE}_megahit_out
