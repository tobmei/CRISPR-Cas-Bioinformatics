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
  bbfastaReference: File?
  bbrightReference: string
  bbminlength: int
  bbk: int?
  bbmink: int?
  # bbktrim: string?
  bbentropy: float?
  bbentropywindow: int?
  bbentropyk: int?
  bbforcetrimmodulo: int?
  bbhammingdistance: int?

steps:
  trimming:
    run: workflow_bbduk.cwl
    scatter: [R1forward, R2reverse]
    scatterMethod: dotproduct
    in:
      R1forward:
        source: R1forwards
      R2reverse:
        source: R2reverses
      bbfastaReference: bbfastaReference
      bbrightReference: bbrightReference
      bbminlength: bbminlength
      bbk: bbk
      bbmink: bbmink
      # bbktrim: bbktrim
      bbentropy: bbentropy
      bbentropywindow: bbentropywindow
      bbentropyk: bbentropyk
      bbforcetrimmodulo: bbforcetrimmodulo
      bbhammingdistance: bbhammingdistance
    out:
      - statistics
      - trimmedR1
      - trimmedR2
      - matchedR1
      - matchedR2

outputs:
  trimmedR1:
    type: File[]
    outputSource: trimming/trimmedR1
  trimmedR2:
    type: File[]
    outputSource: trimming/trimmedR2
  matchedR1:
    type: File[]
    outputSource: trimming/matchedR1
  matchedR2:
    type: File[]
    outputSource: trimming/matchedR2
  statistics:
    type: File[]
    outputSource: trimming/statistics
