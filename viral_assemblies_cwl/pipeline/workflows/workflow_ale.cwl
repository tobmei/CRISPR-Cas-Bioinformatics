cwlVersion: v1.0
class: Workflow
# requirements:
#   MultipleInputFeatureRequirement: {}

inputs:
  R1forward: File
  R2reverse: File
  assembly: File

steps:
  mapReads:
    run: tools/bbmap.cwl
    in:
      forward: R1forward
      reverse: R2reverse
      reference: assembly
      outFileSuffix:
        default: ''
    out:
      - stdout
      - stats
      - covstats
      # - basecov
      - bincov
      - covhist

  sortSam:
    run: tools/samtools.cwl
    in:
      inMapping: mapReads/stdout
    out:
      - sortedBam

  ale:
    run: tools/ale.cwl
    in:
      assembly: assembly
      sam: sortSam/sortedBam
    out:
      - aleOutput

outputs:
  mappingStats:
    type: File
    outputSource: mapReads/stats
  covStats:
    type: File
    outputSource: mapReads/covstats
  mappingCovhist:
    type: File
    outputSource: mapReads/covhist
  mappingBincov:
    type: File
    outputSource: mapReads/bincov
  # mappingBasecov:
  #   type: File
  #   outputSource: mapReads/basecov
  sortedMapping:
    type: File
    outputSource: sortSam/sortedBam
  aleOut:
    type: File
    outputSource: ale/aleOutput
