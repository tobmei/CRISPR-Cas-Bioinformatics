cwlVersion: v1.0
class: Workflow
requirements:
#   MultipleInputFeatureRequirement: {}
  - class: SubworkflowFeatureRequirement

inputs:
  R1forward: File
  R2reverse: File
  megaKmin: int?
  megaKmax: int?
  megaKstep: int?
  megaMinCount: int?
  megaNoMercy: boolean?
  megaNoBubble: boolean?
  megaMergeLevel: float[]?
  megaPruneLevel: int?
  megaLowLocalRatio: float?
  megaMaxTipLens: int?
  megaNoLocal: boolean?
  megaKmin1Pass: boolean?

steps:
  megahit:
    run: tools/megahit.cwl
    in:
      forward: R1forward
      reverse: R2reverse
      kMin: megaKmin
      kMax: megaKmax
      kStep: megaKstep
      minCount: megaMinCount
      noMercy: megaNoMercy
      noBubble: megaNoBubble
      mergeLevel: megaMergeLevel
      pruneLevel: megaPruneLevel
      lowLocalRatio: megaLowLocalRatio
      maxTipLens: megaMaxTipLens
      noLocal: megaNoLocal
      kmin1Pass: megaKmin1Pass
    out:
      - assembly
      - log

  # ale:
  #   run: workflow_ale.cwl
  #   in:
  #     assembly: megahit/assembly
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
    outputSource: megahit/assembly
  megahitLog:
    type: File
    outputSource: megahit/log
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
