cwlVersion: v1.0
class: Workflow
requirements:
#   MultipleInputFeatureRequirement: {}
  - class: SubworkflowFeatureRequirement

inputs:
  R1forward: File
  R2reverse: File
  kList: int[]
  disableRR: boolean?

steps:
  assembly:
    run: tools/metaspades.cwl
    in:
      forward: R1forward
      reverse: R2reverse
      kList: kList
      disableRR: disableRR
    out:
      - contigs
      # - scaffolds
      - log

  # ale:
  #   run: workflow_ale.cwl
  #   in:
  #     assembly: assembly/contigs
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
    outputSource: assembly/contigs
  megahitLog:
    type: File
    outputSource: assembly/log
  # scaffolds:
  #   type: File
  #   outputSource: assembly/scaffolds
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
