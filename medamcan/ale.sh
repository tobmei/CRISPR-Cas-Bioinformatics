#!/bin/bash
#SBATCH --job-name=ale
##SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
##SBATCH --spread-job
#SBATCH --exclude=benz,daimler,maybach
#SBATCH --array=0-59
#SBATCH --mem-per-cpu=12GB
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=tobias.meier@ibvt.uni-stuttgart.de
#SBATCH --output=slurm-%A_%a.out

# input directories and reads
JOB_FILES=(/data/tobias/assembly_jobs_megahit/*)
JOB="${JOB_FILES[$SLURM_ARRAY_TASK_ID]}"

#SAMPLE=nancy
SAMPLE=bioreaktor

OUT_DIR=(${PWD})
echo "out dir: ${OUT_DIR}"
BASE="$(basename "${JOB}")"

L=1kb
#L=5kb
#BAM=/data/tobias/optimized_assembler/assemblies/viral_reference_assemblies_new/megahit/${SAMPLE}_mapping/${BASE}_mapped.bam
BAM=/data/tobias/optimized_assembler/assemblies/viral_reference_assemblies_new/megahit/${SAMPLE}_mapping_${L}/${BASE}_mapped.bam
#CONTIGS=/data/tobias/optimized_assembler/assemblies/viral_reference_assemblies_new/megahit/${SAMPLE}/${BASE}_megahit_out/final.contigs.fa
CONTIGS=/data/tobias/optimized_assembler/assemblies/viral_reference_assemblies_new/megahit/${SAMPLE}/contigs_by_length/${BASE}_final_contigs_${L}.fasta

echo "job ID: ${SLURM_JOB_ID}"
echo "array job ID: ${SLURM_ARRAY_JOB_ID}"
echo "array task ID: ${SLURM_ARRAY_TASK_ID}"
echo "array task count: ${SLURM_ARRAY_TASK_COUNT}"
echo "array task min: ${SLURM_ARRAY_TASK_MIN}"
echo "array task max: ${SLURM_ARRAY_TASK_MAX}"

/home/tmeier/tools/ALE/src/./ALE --nout --metagenome "${BAM}" "${CONTIGS}" "${OUT_DIR}"/"${BASE}"_ALEout.txt