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
    # dockerPull: quay.io/biocontainers/kraken2:2.0.7_beta--pl526h6bb024c_3
    dockerImageId: 413f33a27c64
label: Metaprob
baseCommand: Metaprob/Release/./Metaprob
arguments:
  - position: 1
    prefix: '-dirOutput'
    valueFrom: 'output'

inputs:
  input:
    type: File[]
    inputBinding:
      prefix: -pi
      position: 2
  numSp:
    type: int?
    default: 2
    label: 'Number expected specie in file. Default: 2'
    inputBinding:
      position: 3
      prefix: '-numSp'
  q:
    type: int?
    default: 30
    label: 'Size of q-mer used to create graph adiacences: Default: 30'
    inputBinding:
      position: 4
      prefix: '-q'
  m:
    type: int?
    default: 5
    label: 'Threshold of shared q-mer to create graph adiacences. Default: 5'
    inputBinding:
      positon: 5
      prefix: '-m'
  ssize:
    type: int?
    default: 9000
    label: 'Max Seed size in each group. Default: 9000'
    inputBinding:
      position: 6
      prefix: '-ssize'
  lmerFreq:
    type: int?
    default: 4
    label: 'Size of L-mer used to compute feature vector. Default: 4'
    inputBinding:
      position: 7
      prefix: '-lmerFreq'
  feature:
    type: int?
    default: 1
    label: 'Feature used to compute. Default: 1'
    inputBinding:
      position: 8
      prefix: '-feature'
  mg:
    type: boolean?
    default: false
    label: 'Only group mode activated (output only the groups created). Default: Not Active'
    inputBinding:
      position: 9
      prefix: '-mg'
  eK:
    type: boolean
    default: true
    label: 'Estimate K for K-means algorithm. Default: Active unless you specify -numSp'
    inputBinding:
      position: 10
      prefix: '-eK'

outputs:
  classifiedR1:
    type: File
    outputBinding:
      glob: 'cseqs_1.fastq.gz'
