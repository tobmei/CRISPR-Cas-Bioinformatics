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
baseCommand: [kallisto index]
arguments:
  - position: 1
    valueFrom: 'kallisto_index'
    prefix: '-i'
  - position: 2
    valueFrom: '--make-unique'
    label: 'Replace repeated target names with unique names'

inputs:
  kmerSize:
    type: int
    default: 31
    label: 'k-mer (odd) length (default: 31, max value: 31)'
    inputBinding:
      position: 2
      prefix: '-k'
  fasta:
    type: File
    inputBinding:
      position: 3

outputs:
  index:
    type: File
    outputBinding:
      glob: 'kallisto_index'
