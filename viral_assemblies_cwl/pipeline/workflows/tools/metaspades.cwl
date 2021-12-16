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
    dockerPull: quay.io/biocontainers/spades:3.13.0--0
label: Spades 3.13.0
baseCommand: spades.py
arguments:
  - position: 1
    prefix: '-t'
    valueFrom: '8'
  # - position: 1
  #   prefix: '-m'
  #   valueFrom: '700'
  - position: 2
    valueFrom: '--meta'
  - position: 6
    prefix: '-o'
    valueFrom: 'metaspades_out'
  # - position: 7
  #   prefix: '--trusted-contigs'
  #   valueFrom: 'trusted_contigs.fasta'
  # - position: 8
  #   prefix: '--untrusted-contigs'
  #   valueFrom: 'untrusted_contigs.fasta'
inputs:
  forward:
    type: File
    inputBinding:
      position: 3
      prefix: '-1'
  reverse:
    type: File
    inputBinding:
      position: 4
      prefix: '-2'
  kList:
    type: int[]
    default: [21,31]
    inputBinding:
      itemSeparator: ','
      position: 5
      prefix: '-k'
  # careful:
  #   type: boolean?
  #   default: false
  #   label: "tries to reduce number of mismatches and short indels"
  #   inputBinding:
  #     position: 9
  #     prefix: '--careful'
  # covCutoff:
  #   type: string?
  #   default: 'off'
  #   label: "coverage cutoff value (a positive float number, or 'auto', or 'off')"
  #   inputBinding:
  #     position: 10
  #     prefix: '--cov-cutoff'
  disableRR:
    type: boolean?
    default: false
    label: "disables repeat resolution stage of assembling"
    inputBinding:
      position: 11
      prefix: '--disable-rr'

outputs:
  contigs:
    type: File
    outputBinding:
      glob: metaspades_out/contigs.fasta
  # scaffolds:
  #   type: File
  #   outputBinding:
  #     glob: metaspades_out/scaffolds.fasta
  log:
    type: File
    outputBinding:
      glob: metaspades_out/spades.log
