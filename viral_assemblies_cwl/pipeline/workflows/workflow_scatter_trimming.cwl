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
  trimHeadcrop:
    type: int?
    label: crop first bases
  trimCrop:
    type: int?
    label: crop to length
  trimLeading:
    type: int
    label: trim leading low quality bases
  trimTrailing:
    type: int
    label: trim trailing low quality bases
  trimSlidingwindow:
    type: string
    label: trim using sliding window
  trimMinlen:
    type: int
    label: miminum length of trimmed read
  trimIlluminaclip: string
  trimIlluminaclip2: string?
  trimIlluminaclip3: string?
  trimIlluminaclip4: string?

steps:
  trimming:
    run: workflow_trimming.cwl
    scatter: [R1forward, R2reverse]
    scatterMethod: dotproduct
    in:
      R1forward:
        source: R1forwards
      R2reverse:
        source: R2reverses
      trimHeadcrop: trimHeadcrop
      trimCrop: trimCrop
      trimLeading: trimLeading
      trimTrailing: trimTrailing
      trimSlidingwindow: trimSlidingwindow
      trimMinlen: trimMinlen
      trimIlluminaclip: trimIlluminaclip
      trimIlluminaclip2: trimIlluminaclip2
      trimIlluminaclip3: trimIlluminaclip3
      #illuminaclip4: trimIlluminaclip4
    out:
      - trimmedR1
      - trimmedR2
      - logging

outputs:
  trimmedForward:
    type: File[]
    outputSource: trimming/trimmedR1
  trimmedReverse:
    type: File[]
    outputSource: trimming/trimmedR2
  logging:
    type: File[]
    outputSource: trimming/logging
