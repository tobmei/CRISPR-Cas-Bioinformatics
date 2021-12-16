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
    dockerPull: quay.io/biocontainers/kraken2:2.0.7_beta--pl526h6bb024c_3
label: diamond
baseCommand: [diamond blastx]
arguments:
  - position: 3
    prefix: '--out'
    valueFrom: 'diamond.matches.tsv'
  - position: 4
    prefix: '--outfmt'
    valueFrom: '6' # (101=SAM, 0=BLAST pairwise, 5=BLAST XML, 6=BLAST tabular, 100=DIAMOND alignment archive (DAA))
  - position: 5
    prefix: '--threads'
    valueFrom: '56'
  - position: 6
    valueFrom: '--sensitive' #recommended for long sequences (e.g. contigs)
  - position: 7
    valueFrom: '--quiet'

inputs:
  diamondDB:
    type: File
    inputBinding:
      prefix: --db
      position: 1
  input:
    type: File
    inputBinding:
      prefix: '--query'
      position: 2

outputs:
  alignment:
    type: File
    outputBinding:
      glob: 'diamond.matches.tsv'
