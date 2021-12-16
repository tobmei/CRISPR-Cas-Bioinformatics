cwlVersion: v1.0
class: CommandLineTool
# requirements:
#   - class: ResourceRequirement
#     coresMin: 56
#     ramMin: 48000
#     tmpdirMin: 8192
#   - class: InlineJavascriptRequirement
hints:
  DockerRequirement:
    dockerPull: insilicodb/kallisto
label: kallisto
baseCommand: [kallisto quant]
arguments:
  - position: 1
    valueFrom: 'kallisto_index'
    prefix: '-i'
  - position: 2
    valueFrom: '.'
    prefix: '-o'
  - position: 3
    prefix: '-t'
    valueFrom: 150

inputs:
  fastq:
    type: File[]
    inputBinding:
      position: 4

outputs:
  abundance:
    type: File
    outputBinding:
      glob: 'abundance.tsv'
  abundanceh5:
    type: File
    outputBinding:
      glob: 'abundance.h5'
  log:
    type: File
    outputBinding:
      glob: 'run_info.json'
