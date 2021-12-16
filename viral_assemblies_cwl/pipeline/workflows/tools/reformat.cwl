cwlVersion: v1.0
class: CommandLineTool
# requirements:
#   - class: ResourceRequirement
#     coresMin: 56
#     ramMin: 24000
#     tmpdirMin: 4096
hints:
  DockerRequirement:
    # dockerPull: virusx/bbmap:36.84--0
    dockerPull: bryce911/bbtools
label: BBMap 36.84
baseCommand: reformat.sh
arguments:
  # - "-Xmx$(runtime.ram)M"
  # - "out=$(inputs.forward.basename).bbmap.bam"
  - "out=$(inputs.forward.basename)_interleaved.fastq"

inputs:
  forward:
    type: File
    inputBinding:
      position: 1
      prefix: 'in1='
      separate: false
  reverse:
    type: File?
    inputBinding:
      position: 2
      prefix: 'in2='
      separate: false

outputs:
  interleaved:
    type: File
    outputBinding:
      glob: "$(inputs.forward.basename)_interleaved.fastq"
