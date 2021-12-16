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
    # dockerPull: loneknightpy/idba
    dockerImageId: myidba
label: IDBA
baseCommand: idba_ud
arguments:
  - '-o'
  - 'idbaud_out'
  - '--num_thread'
  - '32'

inputs:
  shortReads:
    type: File?
    label: "interleaved fasta short reads <=250"
    inputBinding:
      position: 2
      prefix: '-r'
  longReads:
    type: File?
    label: "interleaved fasta long reads >=250"
    inputBinding:
      position: 3
      prefix: '-l'
  minK:
    type: int?
    default: 20
    label: "<=124"
    inputBinding:
      position: 4
      prefix: '--mink'
  maxK:
    type: int?
    default: 100
    label: "<=124"
    inputBinding:
      position: 5
      prefix: '--maxk'
  step:
    type: int?
    default: 20
    label: "increment of k-mer of each iteration"
    inputBinding:
      position: 5
      prefix: '--step'
  innerMinK:
    type: int?
    default: 10
    label: "inner minimum k value "
    inputBinding:
      position: 6
      prefix: '--inner_mink'
  innerStep:
    type: int?
    default: 5
    label: "inner increment of k-mer"
    inputBinding:
      position: 7
      prefix: '--inner_step'
  prefixLenght:
    type: int?
    default: 3
    label: "prefix length used to build sub k-mer table"
    inputBinding:
      position: 8
      prefix: '--prefix'
  minCount:
    type: int?
    default: 2
    label: "minimum multiplicity for filtering k-mer when building the graph "
    inputBinding:
      position: 9
      prefix: '--min_count'
  minSupport:
    type: int?
    default: 1
    label: "minimum support in each iteration"
    inputBinding:
      position: 10
      prefix: '--min_support'
  seedKmer:
    type: int?
    default: 30
    label: "seed kmer size for alignment"
    inputBinding:
      position: 11
      prefix: '--seed_kmer'
  minConitg:
    type: int?
    default: 200
    label: "minimum size of contig"
    inputBinding:
      position: 12
      prefix: '--min_contig'
  similar:
    type: float?
    default: 0.95
    label: "similarity for alignment"
    inputBinding:
      position: 13
      prefix: '--similar'
  maxMismatch:
    type: int?
    default: 3
    label: "max mismatch of error correction"
    inputBinding:
      position: 14
      prefix: '--max_mismatch'
  minPairs:
    type: int?
    default: 3
    label: "minimum number of pairs"
    inputBinding:
      position: 15
      prefix: '--min_pairs'
  noBubble:
    type: boolean?
    default: false
    label: "do not merge bubble "
    inputBinding:
      position: 16
      prefix: '--no_bubble'
  noLocal:
    type: boolean?
    default: false
    label: "do not use local assembly"
    inputBinding:
      position: 17
      prefix: '--no_local'
  noCoverage:
    type: boolean?
    default: false
    label: "do not iterate on coverage"
    inputBinding:
      position: 18
      prefix: '--no_coverage'
  noCorrection:
    type: boolean?
    default: false
    label: "do not do correction"
    inputBinding:
      position: 19
      prefix: '--no_correction'
  preCorrection:
    type: boolean?
    default: false
    label: "perform pre-correction before assembly"
    inputBinding:
      position: 20
      prefix: '--pre_correction'

outputs:
  contigs:
    type: File
    outputBinding:
      glob: idbaud_out/contig.fa
  scaffolds:
    type: File
    outputBinding:
      glob: idbaud_out/scaffold.fa
  log:
    type: File
    outputBinding:
      glob: idbaud_out/log
