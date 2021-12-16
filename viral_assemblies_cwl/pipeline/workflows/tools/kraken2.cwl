cwlVersion: v1.0
class: CommandLineTool
requirements:
  InitialWorkDirRequirement:
      listing:
        - $(inputs.krakenDB)
#   - class: ResourceRequirement
#     coresMin: 56
#     ramMin: 48000
#     tmpdirMin: 8192
#   - class: InlineJavascriptRequirement
hints:
  DockerRequirement:
    dockerPull: quay.io/biocontainers/kraken2:2.0.7_beta--pl526h6bb024c_3
label: Kraken 2
baseCommand: kraken2
arguments:
  - position: 2
    valueFrom: '--paired'
  - position: 2
    prefix: '--classified-out'
    valueFrom: 'cseqs#.fastq'
  - position: 3
    prefix: '--unclassified-out'
    valueFrom: 'useqs#.fastq'
  - position: 4
    prefix: '--output'
    valueFrom: 'output.txt'
  - position: 5
    prefix: '--report'
    valueFrom: 'report.txt'
  - position: 6
    prefix: '--threads'
    valueFrom: '56'

inputs:
  krakenDB:
    type: Directory
    inputBinding:
      prefix: --db
      separate: true
      position: 1
  confidence:
    type: float?
    default: 0.0
    inputBinding:
      prefix: '--confidence'
      position: 1
  R1forward:
    type: File
    inputBinding:
      position: 7
  R2reverse:
    type: File
    inputBinding:
      position: 8

outputs:
  classifiedR1:
    type: File
    outputBinding:
      glob: 'cseqs_1.fastq.gz'
  classifiedR2:
    type: File
    outputBinding:
      glob: 'cseqs_2.fastq.gz'
  unclassifiedR1:
    type: File
    outputBinding:
      glob: 'useqs_1.fastq.gz'
  unclassifiedR2:
    type: File
    outputBinding:
      glob: 'useqs_2.fastq.gz'
  output:
    type: File
    outputBinding:
      glob: 'output.txt'
  report:
    type: File
    outputBinding:
      glob: 'report.txt'
