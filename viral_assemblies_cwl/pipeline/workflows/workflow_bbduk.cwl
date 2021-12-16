cwlVersion: v1.0
class: Workflow
# requirements:
#   MultipleInputFeatureRequirement: {}

inputs:
  R1forward: File
  R2reverse: File
  bbfastaReference: File?
  bbrightReference: string
  bbminlength: int?
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
    run: tools/bbduk.cwl
    in:
      forward: R1forward
      reverse: R2reverse
      fastaReference: bbfastaReference
      rightReference: bbrightReference
      minlength: bbminlength
      k: bbk
      mink: bbmink
      # ktrim: bbktrim
      entropy: bbentropy
      entropywindow: bbentropywindow
      entropyk: bbentropyk
      forcetrimmodulo: bbforcetrimmodulo
      hammingdistance: bbhammingdistance
    out:
      - stats
      - trimmedR1
      - trimmedR2
      - matchedR1
      - matchedR2

outputs:
  trimmedR1:
    type: File
    outputSource: trimming/trimmedR1
  trimmedR2:
    type: File
    outputSource: trimming/trimmedR2
  matchedR1:
    type: File
    outputSource: trimming/matchedR1
  matchedR2:
    type: File
    outputSource: trimming/matchedR2
  statistics:
    type: File
    outputSource: trimming/stats
