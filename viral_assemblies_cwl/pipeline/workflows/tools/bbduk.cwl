cwlVersion: v1.0
class: CommandLineTool
# requirements:
#   - class: ResourceRequirement
#     coresMin: 56
#     ramMin: 24000
#     tmpdirMin: 4096
hints:
  DockerRequirement:
    dockerPull: virusx/bbmap:36.84--0
label: BBMap 36.84
baseCommand: bbduk2.sh
arguments:
  - "-Xmx120G" #using Xmx$(runtime.RAM)M did not work as well as letting bbduk2 decide
  - "prealloc=t"
  - "stats=$(inputs.forward.basename).stats"
  - "out1=$(inputs.forward.basename).clean1.fastq"
  - "out2=$(inputs.forward.basename).clean2.fastq"
  - "outm=$(inputs.forward.basename).outmatched1.fastq"
  - "outm2=$(inputs.forward.basename).outmatched2.fastq"

inputs:
  forward:
    type: File
    inputBinding:
      position: 1
      prefix: 'in='
      separate: false
  reverse:
    type: File?
    inputBinding:
      position: 2
      prefix: 'in2='
      separate: false
  fastaReference:
    type: File?
    label: "Comma-delimited list of fasta reference files for filtering"
    inputBinding:
      position: 5
      prefix: 'fref='
      separate: false
  rightReference:
    type: string
    label: "Comma-delimited list of fasta reference files for right-trimming."
    inputBinding:
      position: 5
      prefix: 'rref='
      separate: false
  leftLiteral:
    type: string?
    label: "Comma-delimited list of literal sequences for left-trimming."
    inputBinding:
      position: 5
      prefix: 'lliteral='
      separate: false
  minlength:
    type: int?
    default: 10
    inputBinding:
      position: 10
      prefix: "minlength="
      separate: false
  k:
    type: int?
    default: 27
    label: "k=27 Kmer length used for finding contaminants.  Contaminants shorter than k will not be found.  k must be at least 1. "
    inputBinding:
      position: 11
      prefix: "k="
      separate: false
  mink:
    type: int?
    default: -1
    label: "Look for shorter kmers at read tips down to this length, when k-trimming or masking.  0 means disabled.  Enabling"
    inputBinding:
      position: 12
      prefix: "mink="
      separate: false
  # ktrim:
  #   type: string?
  #   default: f
  #   inputBinding:
  #     position: 6
  #     prefix: "ktrim="
  #     separate: false
  entropy:
    type: float?
    default: -1.0
    label: "Set between 0 and 1 to filter reads with entropy below that value.  Higher is more stringent."
    inputBinding:
      position: 7
      prefix: "entropy="
      separate: false
  entropywindow:
    type: int?
    default: 50
    label: "Calculate entropy using a sliding window of this length."
    inputBinding:
      position: 8
      prefix: "entropywindow="
      separate: false
  entropyk:
    type: int?
    # default: 5
    label: "Calculate entropy using kmers of this length. "
    inputBinding:
      position: 9
      prefix: "entropyk="
      separate: false
  forcetrimmodulo:
    type: int?
    default: 0
    label: "(ftm) If positive, right-trim length to be equal to zero, modulo this number."
    inputBinding:
      position: 13
      prefix: "forcetrimmod="
      separate: false
  hammingdistance:
    type: int?
    default: 0
    label: "(hdist) Maximum Hamming distance for ref kmers (subs only). Memory use is proportional to (3*K)^hdist"
    inputBinding:
      position: 14
      prefix: "hdist="
      separate: false

outputs:
  stats:
    type: File
    outputBinding:
      glob: "$(inputs.forward.basename).stats"
  trimmedR1:
    type: File
    outputBinding:
      glob: "$(inputs.forward.basename).clean1.fastq"
  trimmedR2:
    type: File
    outputBinding:
      glob: "$(inputs.forward.basename).clean2.fastq"
  matchedR1:
    type: File
    outputBinding:
      glob: "$(inputs.forward.basename).outmatched1.fastq"
  matchedR2:
    type: File
    outputBinding:
      glob: "$(inputs.forward.basename).outmatched2.fastq"
