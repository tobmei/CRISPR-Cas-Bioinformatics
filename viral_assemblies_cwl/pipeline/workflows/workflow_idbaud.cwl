cwlVersion: v1.0
class: Workflow
requirements:
#   MultipleInputFeatureRequirement: {}
  - class: SubworkflowFeatureRequirement

inputs:
  R1forward: File
  R2reverse: File
  minK: int
  maxK: int
  step: int
  innerMinK: int?
  innerStep: int?
  prefixLenght: int?
  minCount: int?
  minSupport: int?
  seedKmer: int?
  minConitg: int?
  similar: float?
  maxMismatch: int?
  minPairs: int?
  noBubble: boolean?
  noLocal: boolean?
  noCoverage: boolean?
  noCorrection: boolean?
  preCorrection: boolean?

steps:
  reformat:
    run: tools/reformat.cwl
    in:
      forward: R1forward
      reverse: R2reverse
    out:
      - interleaved

  idba:
    run: tools/idba.cwl
    in:
      shortReads: reformat/interleaved
      minK: minK
      maxK: maxK
      step: step
      innerMinK: innerMinK
      innerStep: innerStep
      prefixLenght: prefixLenght
      minCount: minCount
      minSupport: minSupport
      seedKmer: seedKmer
      minConitg: minConitg
      similar: similar
      maxMismatch: maxMismatch
      minPairs: minPairs
      noBubble: noBubble
      noLocal: noLocal
      noCoverage: noCoverage
      noCorrection: noCorrection
      preCorrection: preCorrection
    out:
      - contigs
      - scaffolds
      - log

  # ale:
  #   run: workflow_ale.cwl
  #   in:
  #     assembly: idba/contigs
  #     R1forward: R1forward
  #     R2reverse: R2reverse
  #
  #   out:
  #     - aleOut
  #     - sortedMapping
  #     - mappingBincov
  #     - mappingCovhist
  #     - covStats
  #     - mappingStats


outputs:
  megahitContigs:
    type: File
    outputSource: idba/contigs
  megahitLog:
    type: File
    outputSource: idba/log
  scaffolds:
    type: File
    outputSource: idba/scaffolds
  # mappingStats:
  #   type: File
  #   outputSource: ale/mappingStats
  # covStats:
  #   type: File
  #   outputSource: ale/covStats
  # mappingCovhist:
  #   type: File
  #   outputSource: ale/mappingCovhist
  # mappingBincov:
  #   type: File
  #   outputSource: ale/mappingBincov
  # sortedMapping:
  #   type: File
  #   outputSource: ale/sortedMapping
  # aleOut:
  #   type: File
  #   outputSource: ale/aleOut
