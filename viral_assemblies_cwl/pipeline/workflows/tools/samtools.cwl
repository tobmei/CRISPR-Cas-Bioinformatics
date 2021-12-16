cwlVersion: v1.0
class: CommandLineTool

hints:
  DockerRequirement:
    dockerPull: quay.io/biocontainers/samtools:1.3.1--5

baseCommand: samtools
arguments:
  - "sort"
  # - "-m"
  # - "$(runtime.ram)M"
  - "-@"
  - "170"
  - "-l"
  - "9"
  - "-o"
  - "$(inputs.inMapping.basename).out.sorted.bam"

inputs:
  inMapping:
    type: File
    streamable: true

outputs:
  sortedBam:
    type: File
    outputBinding:
      glob: '$(inputs.inMapping.basename).out.sorted.bam'

stdin: '$(inputs.inMapping.path)'
