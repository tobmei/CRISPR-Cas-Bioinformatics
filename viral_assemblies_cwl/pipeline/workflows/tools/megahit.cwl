cwlVersion: v1.0
class: CommandLineTool
requirements:
  # - class: ResourceRequirement
  #   coresMin: 56
  #   ramMin: 48000
  #   tmpdirMin: 8192
  - class: InlineJavascriptRequirement
hints:
  DockerRequirement:
    dockerPull: quay.io/biocontainers/megahit:1.1.3--py35_0
label: MEGAHIT 1.1.3
baseCommand: megahit
arguments:
  - position: 1
    prefix: '-t'
    valueFrom: '176'
  - position: 2
    prefix: '--out-prefix'
    valueFrom: '$(inputs.forward.basename).megahit'

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
  minContigLength:
    type: int?
    default: 200
    inputBinding:
      position: 6
      prefix: '--min-contig-len'
  kStep:
    type: int?
    default: 20
    label: '<= 28'
    inputBinding:
      position: 7
      prefix: '--k-step'
  kMin:
    type: int?
    default: 21
    label: '<= 127'
    inputBinding:
      position: 7
      prefix: '--k-min'
  kMax:
    type: int?
    default: 99
    label: '<= 127'
    inputBinding:
      position: 8
      prefix: '--k-max'
  minCount:
    type: int?
    default: 2
    label: 'minimum multiplicity for filtering (k_min+1)-mers'
    inputBinding:
      position: 9
      prefix: '--min-count'
  noMercy:
    type: boolean?
    default: false
    label: 'do not add mercy kmers'
    inputBinding:
      position: 10
      prefix: '--no-mercy'
  noBubble:
    type: boolean?
    default: false
    label: 'do not merge bubbles'
    inputBinding:
      position: 11
      prefix: '--no-bubble'
  mergeLevel:
    type: float[]?
    default: [20.0,0.98]
    label: 'merge complex bubbles of length <= l*kmer_size and similarity >= s'
    inputBinding:
      position: 12
      prefix: '--merge-level'
      itemSeparator: ','
  pruneLevel:
    type: int?
    default: 2
    label: 'strength of local low depth pruning (0-2)'
    inputBinding:
      position: 13
      prefix: '--prune-level'
  lowLocalRatio:
    type: float?
    default: 0.2
    label: 'ratio threshold to define low local coverage contigs'
    inputBinding:
      position: 14
      prefix: '--low-local-ratio'
  maxTipLens:
    type: int?
    default: 2
    label: 'remove tips less than this value; default 2*k for iteration of kmer_size=k'
    inputBinding:
      position: 15
      prefix: '--max-tip-len'
  noLocal:
    type: boolean?
    default: false
    label: 'disable local assembly'
    inputBinding:
      position: 16
      prefix: '--no-local'
  kmin1Pass:
    type: boolean?
    default: false
    label: 'use 1pass mode to build SdBG of k_min - more memory efficient for ultra low-depth data (e.g. soil)'
    inputBinding:
      position: 17
      prefix: '--kmin-1pass'
outputs:
  assembly:
    type: File
    outputBinding:
      glob: megahit_out/$(inputs.forward.basename).megahit.contigs.fa
  log:
    type: File
    outputBinding:
      glob: megahit_out/$(inputs.forward.basename).megahit.log
