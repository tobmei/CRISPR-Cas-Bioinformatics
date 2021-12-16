cwlVersion: v1.0
class: Workflow
requirements:
- class: InlineJavascriptRequirement
- class: ScatterFeatureRequirement
- class: StepInputExpressionRequirement
- class: SubworkflowFeatureRequirement

inputs:
  R1forwards: File[]
  R2reverses: File[]
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
    run: workflow_megahit.cwl
    scatter: [R1forward, R2reverse]
    scatterMethod: dotproduct
    in:
      R1forward:
        source: R1forwards
      R2reverse:
        source: R2reverses
      megaKmin: megaKmin
      megaKmax: megaKmax
      megaKstep: megaKstep
      megaMinCount: megaMinCount
      megaNoMercy: megaNoMercy
      megaNoBubble: megaNoBubble
      megaMergeLevel: megaMergeLevel
      megaPruneLevel: megaPruneLevel
      megaLowLocalRatio: megaLowLocalRatio
      megaMaxTipLens: megaMaxTipLens
      megaNoLocal: megaNoLocal
      megaKmin1Pass: megaKmin1Pass
    out:
      - megahitContigs
      - megahitLog
      - mappingStats
      - covStats
      - mappingCovhist
      - mappingBincov
      - sortedMapping
      - aleOut


outputs:
  megahitContigs:
    type: File[]
    outputSource: megahit/megahitContigs
  megahitLog:
    type: File[]
    outputSource: megahit/megahitLog
  mappingStats:
    type: File[]
    outputSource: megahit/mappingStats
  covStats:
    type: File[]
    outputSource: megahit/covStats
  mappingCovhist:
    type: File[]
    outputSource: megahit/mappingCovhist
  mappingBincov:
    type: File[]
    outputSource: megahit/mappingBincov
  # mappingBasecov:
  #   type: File[]
  #   outputSource: megahit/mappingBasecov
  # sortedMapping:
  #   type: File[]
  #   outputSource: megahit/sortedMapping
  # aleOut:
  #   type: File[]
  #   outputSource: megahit/aleOut
  # aleOutPlot:
  #   type: File
  #   outputSource: alePlot/aleOutPlot
  # alePlotStdout:
  #   type: File[]
  #   outputSource: alePlot/alePlotStdout
  # alePlotStderr:
  #   type: File[]
  #   outputSource: alePlot/alePlotStderr
