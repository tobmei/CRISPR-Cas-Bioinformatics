cwlVersion: v1.0
class: CommandLineTool
# requirements:
  # - class: ResourceRequirement
  #   coresMin: 56
  #   coresMax: 56
  #   ramMin: 2048
  #   tmpdirMin: 4096
  # InitialWorkDirRequirement: # fastqc wants to write output into input file directory
  #     listing:
  #       - $(inputs.fastq1)
  #       - $(inputs.fastq2)

hints:
  DockerRequirement:
    dockerPull: quay.io/biocontainers/fastqc:0.11.8--1
label: Fastqc 0.11.8
baseCommand: fastqc
arguments:
  - position: 1
    prefix: '--outdir'
    valueFrom: $(runtime.outdir)
  - position: 2
    prefix: '--threads'
    valueFrom: '56'
inputs:
  fastq1:
    type: File
    inputBinding:
      position: 3
  fastq2:
    type: File
    inputBinding:
      position: 4


outputs:
  html:
    type: File[]
    outputBinding:
      glob: '*.html'
  zip:
    type: File[]
    outputBinding:
      glob: '*.zip'
