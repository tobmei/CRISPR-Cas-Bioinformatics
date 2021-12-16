#!/bin/bash
#SBATCH --job-name=bbmap
##SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
##SBATCH --spread-job
#SBATCH --exclude=benz,daimler,maybach
#SBATCH --array=0-59
#SBATCH --mem-per-cpu=4GB
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=tobias.meier@ibvt.uni-stuttgart.de
#SBATCH --output=slurm-%A_%a.out

# input directories and reads
JOB_FILES=(/data/tobias/assembly_jobs_megahit/*)
JOB="${JOB_FILES[$SLURM_ARRAY_TASK_ID]}"

SAMPLE=nancy
#SAMPLE=bioreaktor

READS_R1=/data/tobias/${SAMPLE}/viral_reads_preprocessed/V_R1.fastq.gz
READS_R2=/data/tobias/${SAMPLE}/viral_reads_preprocessed/V_R2.fastq.gz

OUT_DIR=(${PWD})
echo "out dir: ${OUT_DIR}"
BASE="$(basename ${JOB})"

#REF=/data/tobias/optimized_assembler/assemblies/viral_reference_assemblies_new/megahit/${SAMPLE}/${BASE}_megahit_out/final.contigs.fa
REF=/data/tobias/optimized_assembler/assemblies/viral_reference_assemblies_new/megahit/${SAMPLE}/contigs_by_length/${BASE}_final_contigs_1kb.fasta
#REF=/data/tobias/optimized_assembler/assemblies/viral_reference_assemblies_new/megahit/${SAMPLE}/contigs_by_length/${BASE}_final_contigs_5kb.fasta

echo "reference: ${REF}"
echo "job ID: ${SLURM_JOB_ID}"
echo "array job ID: ${SLURM_ARRAY_JOB_ID}"
echo "array task ID: ${SLURM_ARRAY_TASK_ID}"
echo "array task count: ${SLURM_ARRAY_TASK_COUNT}"
echo "array task min: ${SLURM_ARRAY_TASK_MIN}"
echo "array task max: ${SLURM_ARRAY_TASK_MAX}"

docker run --rm --user 10018:1000 -v ${REF}:/contigs.fa -v ${READS_R1}:/readR1 -v ${READS_R2}:/readR2 -v ${OUT_DIR}:/out 7a9dfabc7c0c bbmap.sh ref=/contigs.fa in=/readR1 in2=/readR2 t=24 nodisk=t covhist=/out/${BASE}_covhist.txt scafstats=/out/${BASE}_scafstats.txt out=/out/"${BASE}"_mapped.sam bamscript=bs.sh; sh bs.sh
#/tools/src/bbmap/./bbmap.sh ref=${REF} in=${READS_R1} in2=${READS_R2} t=24 out=${OUT_DIR}/"${BASE}"_mapped.bam