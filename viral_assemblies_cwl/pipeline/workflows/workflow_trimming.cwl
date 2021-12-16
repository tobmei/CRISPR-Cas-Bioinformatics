cwlVersion: v1.0
class: Workflow
# requirements:
#   MultipleInputFeatureRequirement: {}

inputs:
  R1forward: File
  R2reverse: File
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
    run: tools/trimmomatic.cwl
    in:
      forward: R1forward
      reverse: R2reverse
      headcrop: trimHeadcrop
      crop: trimCrop
      leading: trimLeading
      trailing: trimTrailing
      slidingwindow: trimSlidingwindow
      minlen: trimMinlen
      illuminaclip: trimIlluminaclip
      illuminaclip2: trimIlluminaclip2
      illuminaclip3: trimIlluminaclip3
      #illuminaclip4: trimIlluminaclip4
    out:
      - forwardPaired
      - forwardUnpaired
      - reversePaired
      - reverseUnpaired
      - log

outputs:
  trimmedR1:
    type: File
    outputSource: trimming/forwardPaired
  trimmedR2:
    type: File
    outputSource: trimming/reversePaired
  logging:
    type: File
    outputSource: trimming/log
