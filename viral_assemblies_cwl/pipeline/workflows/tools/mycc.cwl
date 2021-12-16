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
    dockerPull: 990210oliver/mycc.docker:v1
label: MyCC
baseCommand: [MyCC.py]
arguments:
  - position: 3
    valueFrom: '-meta'
    label: 'Change to meta mode of Prodigal. [default: single]'

inputs:
  contigFile:
    type: File
    label: 'contig input file'
    inputBinding:
      position: 1
  mer:
    type: String?
    default: '4mer'
    label: '4mer/5mer/56mer'
    inputBinding:
      position: 2
  coverageFile:
    type: File?
    label: 'file with coverage information'
    inputBinding:
      prefix: '-a'
  minContigLength:
    type: int?
    default: 1000
    label: 'Minimum contig length. [defaults: 1000 bp]'
    inputBinding:
      prefix: '-t'
  contigFrac:
    type: float?
    label: 'A fraction of contigs for the first-stage clustering. [default: 0.7]'
    default: 0.7
    inputBinding:
      prefix: '-lt'
  firstStage:
    type: int?
    label: 'Minimum contig lengh for first stage clustering. [bp]'
    inputBinding:
      prefix: '-ct'
  perplex:
    type: int?
    default: 20
    label: 'Perplexity for BH-SNE. [default: 20, range between 5 and 50]'
    inputBinding:
      prefix: '-p'
  maxDist:
    type: int?
    default: 500
    label: 'Maximum distance for sparse format of affinity propagation. [default: 500]'
    inputBinding:
      prefix: '-st'

outputs:
  clusters:
    type: File[]
    outputBinding:
      glob: 'Cluster.*.fasta'
  summary:
    type: File
    outputBinding:
      glob: 'Cluster.summary'
  coords:
    type: File
    outputBinding:
      glob: 'MyCluster.coords'
  pdf:
    type: File
    outputBinding:
      glob: 'MyCluster.pdf'
  log:
    type: File
    outputBinding:
      glob: 'log'
